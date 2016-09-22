from twilio.rest import TwilioRestClient
import requests
import time

ACCOUNT_SID = 'ACcdfe405c4e902b22a0f7fa81fa20befa' # Replace with your Twilio account sid
AUTH_TOKEN = 'da58093e1bb933635d54311a2695f404' # Replace with your Twilio auth token

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

# JSON API URL for checking availability status
check_url = "http://www.apple.com/shop/retail/pickup-message?parts.0=MN5L2LL%2FA&location=San+Francisco%2C+CA&little=true&cppart=TMOBILE%2FUS"

# Track the last pickup status so we know when it changes
lastPickupStatus = ""

while True:

  try:

    # Fetch data about pickup status
    body = requests.get(check_url)
    data = body.json()
    availableStores = []
    for store in data['body']['stores']:
      status = store["partsAvailability"]["MN562LL/A"]["storePickupQuote"]
      if status != "Currently unavailable":
        availableStores.append({
          "name": store["storeName"],
          "status": status
        })

    # If it's available, see if we need to send a text
    if len(availableStores) > 0:
      pickupStatus = ", ".join([
        "%s: %s" % (
          store["name"], store["status"]
        ) for store in availableStores
      ])

      # if the pickup status has changed since we last sent a text,
      # send another text
      if pickupStatus != lastPickupStatus:
        lastPickupStatus = pickupStatus
        client.messages.create(
          to='+14158233568', # Replace with your phone number
          from_='+13345390168', # Replace with the number from Twilio
          body='iPhone 7 Plus Pickup Status: %s' % pickupStatus
        )

  # Catch-all, mostly just in case we have a network error
  # This is sloppy but functional, remember?
  except Exception as e:
    print e

  # Only check once a minute
  time.sleep(60)
