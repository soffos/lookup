import re
import requests

def print_addresses(address_list):
  for address in address_list:
    print(address)
  print("{} IPv4 address found.".format(len(address_list)))

def print_filtered_addresses(address_list):
  printable = filter_addresses(address_list)
  if printable:
    for addr in printable:
      print(addr)
  else:
    return

def filter_addresses(address_list):
  ops = {
    "contains": lambda p,addr: p in addr,
    "startsWith": lambda p,addr: addr.startsWith(p),
    "endsWith": lambda p,addr: addr.endsWith(p),
    "greaterThan": lambda p,addr: addr > p,
    "lessThan": lambda p,addr: addr < p
  }
  print("You can use the custom language to filter results as needed.")
  query = input("Please enter your query:")
  queryComp = query.split()
  if len(queryComp) > 1 and queryComp[0] in ops:
    filteredAddrs = []
    for address in address_list:
      if queryComp[0] in ["greaterThan","lessThan"]:
        pAddrComp = list(map(int, queryComp[1].split('.')))
        tAddrComp = list(map(int, address.split('.')))
        if ops[queryComp[0]](pAddrComp, tAddrComp):
          filteredAddrs.append(address)
      elif ops[queryComp[0]](queryComp[1], address):
        filteredAddrs.append(address)
    return filteredAddrs
  else:
    print("Invalid query parameters. Please refer to the documentation.")
    return None

def geoip_lookup(address_list):
  print("This tool uses free API endpoints, " +
        "which have a limited free tier before access is restricted. " +
        "Please filter the IP addresses you want to look up " +
        "prior to performing the GeoIP lookup to avoid exhausting the resources.")
  geoIpEpPat = "https://api.ipdata.co/{}"
  lookupAddrs = filter_addresses(address_list)
  for address in lookupAddrs:
    resp = requests.get(geoIpEpPat.format(address))
    print(resp.json())

def rdap_lookup(address_list):
  print("Please filter the IP addresses you want to look up " +
        "prior to performing the RDAP lookup to minimize requests sent to the ARIN API.")
  rdapIpEpPat = "https://rdap.arin.net/registry/ip/{}"
  lookupAddrs = filter_addresses(address_list)
  for address in lookupAddrs:
    resp = requests.get(rdapIpEpPat.format(address))
    print(resp.json())

if __name__ == "__main__":
  print("Welcome to cystalker.\n" +
        "Please begin by entering the path to a file to parse")
  fPath = input()
  try:
    inputFile = open(fPath, 'r')
    fileContents = inputFile.read()
    inputFile.close()
  except OSError as e:
    print("Problem opening file: {}".format(repr(e)))
    exit()
  
  ipv4Addrs = re.findall(r"\b((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:(?<!\.)\b|\.)){4})", fileContents)
  
  ops = [
    print_addresses,
    print_filtered_addresses,
    geoip_lookup,
    rdap_lookup
  ]
  while True:
    print("What would you like to do?\n" +
          "[0]: Print all addresses found.\n" +
          "[1]: Filter addresses and print selection.\n" +
          "[2]: Perform GeoIP lookup on addresses found.\n" +
          "[3]: Perform RDAP lookup on addresses found.\n" +
          "[4]: Exit program.\n")
    op = int(input())
    if op < len(ops):
      ops[op](ipv4Addrs)
    elif op==4:
      exit()
    else:
      "Invalid input detected. Please select one of the provided options."