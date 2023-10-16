import requests
from heyoo import WhatsApp

# Function to send WhatsApp message using Heyoo
def send_whatsapp_message(cid, message):
    print('Sending message...');
    messenger.send_message(message, '524432718336')

# Function to check visa wait times and send WhatsApp message if conditions are met
def check_visa_wait_times(cid):
    url = f"https://travel.state.gov/content/travel/resources/database/database.getVisaWaitTimes.html?cid={cid}&aid=VisaWaitTimesHomePage"

    try:
        response = requests.get(url)
        response.raise_for_status()

        # Extracting visa wait times from the response
        wait_times_str = response.text
        wait_times_str = wait_times_str.replace('\r\n', '')  # Remove extra characters
        wait_times_str = ''.join(char for char in wait_times_str if char.isdigit() or char.isspace())  # Keep only digits and spaces
        wait_times = [int(part) for part in wait_times_str.split()]

        # Checking the condition for the first wait time
        if wait_times and wait_times[0] <= 100:
            message = f"Citas disponibles en {cid_name_mapping[cid]} ({cid}) con un tiempo de espera de menos de 100 días: {wait_times[0]} días"
            send_whatsapp_message(cid, message)
        else:
            print('No hay citas disponibles')

    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")



# Heyoo configuration
token = 'EAAMQ94qZAFCkBO8RzysNhGDAiYn6XPloC8RzZBzILU1Gmp0Hc6VuRAM08p3oJtzXkrDhIV1opJKt4BfyOJCGFxMLXgZC8Lpw7rFtB8iDMvF6RzKIIvGyRCN0RLGxNWRsBH8G34NFCE1MCZBZAEjwuLVG5qBZAtyeml0MlAZCdZAkYemDpAYmumQnYEwxBV2Rb5TpGIdcBcn1h7qfTUgXHMgZD'
phone_number_id = '143039462228107'
messenger = WhatsApp(token, phone_number_id=phone_number_id)

# List of CIDs to check
cids = ["tijuana", "P72", "P135", "P130", "P131"]
cid_name_mapping = {
    "tijuana": "Tijuana",
    "P72": "Guadalajara",
    "P135": "Monterrey",
    "P130": "Merida",
    "P131": "Mexico"
}

# Iterate through CIDs and check visa wait times
for cid in cids:
    check_visa_wait_times(cid)
