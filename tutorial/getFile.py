import urllib

testfile = urllib.URLopener()
testfile.retrieve("https://app.relateiq.com/svc/v1/entitylists/54f14ea2e4b0c7427aeaa17f/export/grid.csv", "grid.csv")