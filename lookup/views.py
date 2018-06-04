from lookup import app
from flask import render_template, request, session, jsonify
import re
import requests

@app.route("/", methods=["GET"])
def index():
  return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
  print(request.files)
  f = request.files['file']
  if f:
    fContent = f.read()
    allAddrs = re.findall(r"\b((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:(?<!\.)\b|\.)){4})", str(fContent))
    session['allAddrs'] = [{'ipv4': ipv4} for ipv4 in allAddrs]
    session['dispAddrs'] = session['allAddrs'][:]
  return index()

@app.route("/addrs_frame", methods=["GET"])
@app.route("/addrs_frame/<desired>", methods=["GET"])
def addrs_frame(desired=None):
  return render_template("frame.html",
                         desired=desired)

@app.route("/reset_filter", methods=["POST"])
def reset_filter():
  session['dispAddrs'] = session['allAddrs']
  return jsonify({"statusCode": "HTTP/2 200 OK"})

@app.route("/filter", methods=["POST"])
def filter():
  requestJson = request.get_json(force=True)
  query = requestJson.get('filter')
  ops = {
    "contains": lambda p,addr: p in addr,
    "startsWith": lambda p,addr: addr.startswith(p),
    "endsWith": lambda p,addr: addr.endswith(p),
    "greaterThan": lambda p,addr: addr > p,
    "lessThan": lambda p,addr: addr < p
  }

  queryComp = query.split()
  if len(queryComp) > 1 and queryComp[0] in ops:
    filteredAddrs = []
    for addressDict in session['allAddrs']:
      address = addressDict['ipv4']
      if queryComp[0] in ["greaterThan","lessThan"]:
        pAddrComp = list(map(int, queryComp[1].split('.')))
        tAddrComp = list(map(int, address.split('.')))
        if ops[queryComp[0]](pAddrComp, tAddrComp):
          filteredAddrs.append(addressDict)
      elif ops[queryComp[0]](queryComp[1], address):
        filteredAddrs.append(addressDict)
    session['dispAddrs'] = filteredAddrs
  return jsonify({"statusCode": "HTTP/2 200 OK"})

@app.route("/geoip", methods=["POST"])
def geoip_lookup():
  geoIpEpPat = "https://api.ipdata.co/{}"
  targetAddrs = session['dispAddrs'][:]
  for idx,address in enumerate(targetAddrs):
    resp = requests.get(geoIpEpPat.format(address['ipv4']))
    targetAddrs[idx]['geoip'] = resp.json()
    targetAddrs[idx].pop('rdap', None)
  session['dispAddrs'] = targetAddrs
  return jsonify({"statusCode": "HTTP/2 200 OK"})

@app.route("/rdap", methods=["POST"])
def rdap_lookup():
  rdapIpEpPat = "https://rdap.arin.net/registry/ip/{}"
  targetAddrs = session['dispAddrs'][:]
  for idx,address in enumerate(targetAddrs):
    resp = requests.get(rdapIpEpPat.format(address['ipv4']))
    targetAddrs[idx]['rdap'] = resp.json()
    targetAddrs[idx].pop('geoip', None)
  session['dispAddrs'] = targetAddrs
  return jsonify({"statusCode": "HTTP/2 200 OK"})
  