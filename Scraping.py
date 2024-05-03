import requests
from bs4 import BeautifulSoup

def scrape_salon_data(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract salon name
        salon_name_element = soup.find('h1', class_='purify_3UeKw5MV+NerIrQNs8HSXA==')
        salon_name = salon_name_element.get_text(strip=True) if salon_name_element else "Salon name not found"
        
        # Extract location
        location_element = soup.find('div', class_='purify_prm7MfDXczhTZvcY5KwOuA==')
        location = location_element.get_text(strip=True) if location_element else "Location not found"
        
        # Extract service names and prices
        services = []
        service_containers = soup.select('#pageSection > div:nth-child(6) > div > ul > li > div > ul > li > div')
        for container in service_containers:
            service_name_element = container.select_one('div.purify_aIF50SidLa4hohq9cO8NHw\=\= > h3')
            service_name = service_name_element.text.strip() if service_name_element else "Service name not found"

            price_element = container.select_one('div.purify_D1SZtxyq0LT9u5Tm8cMYuw\=\= > div > div > div.purify_lPTOnTJKdGtFsWiIA3TUBA\=\= > div:nth-child(1) > div')
            price = price_element.text.strip() if price_element else "Price not found"

            services.append({'Service': service_name, 'Price': price})

        
        # Extract salon work images
        images = []
        image_elements = soup.select('#pageSection > div:nth-child(8) > div > div > div.purify_g-cCOjzOdfQE53GMFgP-8g > div')
        for image_element in image_elements:
            image_url = image_element.find('img')['src']
            images.append(image_url)
        
        # Extract phone number
        phone_element = soup.select_one('#page > main > div > div.pageView > div.purify_ttvfWqhvGJS6e-ZjgDKmFg\=\= > div > aside > div > div > div > section.purify_VbEpwGf39H6\+5nz2giTf5w\=\=.purify_JE8JU2MBLhR-2Y4IcQ249A\=\= > div.purify_aTkNPTKgp2lm7u4xe5cu1Q\=\=.purify_Sardy6hfiet162IZ2pYFPA\=\=.purify_f9tJlQGTtqZe8Hg0f7oQhg\=\=.purify_ROCe7iP3wONNs4wBWGPEMA\=\=')
        phone_number = phone_element.text.strip().replace('\n', ' ').replace('Call', '').strip() if phone_element else "Phone number not found"
        
        # Extract work days and hours
        work_days_element = soup.select_one('#page > main > div > div.pageView > div.purify_ttvfWqhvGJS6e-ZjgDKmFg\=\= > div > aside > div > div > div > section.purify_VbEpwGf39H6\+5nz2giTf5w\=\=.purify_JE8JU2MBLhR-2Y4IcQ249A\=\= > div.purify_Fs277dX\+zCIr8ZfNikeEwg\=\= > div.purify_GQgfOFrDrO--OhEuBSRkDw\=\=')
        work_days_and_hours = work_days_element.text.strip() if work_days_element else "Work hours not found"
        

        # Extract social media links
        social_media_links_element = soup.select_one('[data-testid="social-media-share-btn"]')
        if social_media_links_element:
            social_media_links = {}
            social_media_elements = social_media_links_element.select('a')
            for social_media_element in social_media_elements:
                platform = social_media_element.select_one('h3').get_text(strip=True)
                link = social_media_element['href']
                social_media_links[platform] = link
        else:
            social_media_links = "Social media links not found"

        print("Social Media Links:")
        if isinstance(social_media_links, dict):
            for platform, link in social_media_links.items():
                print(f"{platform}: {link}")
        else:
            print(social_media_links)

        
        # Extract reviews count
        review_count_div = soup.find('div', class_='purify_aNo2rKM2GaqragdL24RFJA== purify_Sardy6hfiet162IZ2pYFPA== purify_m9mNOPjpHD0tNTW6GC+hEw==')
        review_count_text = review_count_div.get_text()
        
        # Extract every review
        reviews = []
        review_elements = soup.select('#reviews-section > div.purify_6I9ICr0-qNOJfxFM4x purify_4JysCXCgTMjx Y9GX0xPjg')
        for review_element in review_elements:
            review_text = review_element.get_text(strip=True)
            reviews.append(review_text)
        
        # Create dictionary to store all the data
        salon_data = {
            'Salon Name': salon_name,
            'Location': location,
            'Services': services,
            'Salon Work Images': images,
            'Phone Number': phone_number,
            'Work Hours': work_days_and_hours,  # Corrected variable name
            'Social Media Links': social_media_links,
            'Reviews Count': reviews_count,
            'Reviews': reviews
        }

        # Return the dictionary containing all the data
        return salon_data
    else:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
        return None

# URL of the specific salon page
salon_url = "https://booksy.com/en-us/843004_luscious-hair_hair-salon_134611_arlington#ba_s=sr_1"
data = scrape_salon_data(salon_url)


# Displaying data in a user-friendly list
if data:
    print("Salon Name:", data['Salon Name'])
    print("Location:", data['Location'])
    print("Phone Number:", data['Phone Number'])
    print("Work Hours:")
    work_hours = data['Work Hours']
    work_hours_lines = work_hours.split('\n')
    for line in work_hours_lines:
        if 'Closed' in line:
            print(line)
        else:
            day_and_hours = line.split(':')
            if len(day_and_hours) == 1:
                print(day_and_hours[0].strip())  # Handle case when no hours are provided
            else:
                day, hours = day_and_hours[0], ':'.join(day_and_hours[1:]).strip()  # Correctly join the hours
                print(f"{day.strip()} {hours}")
    print("Social Media Links:")
    if isinstance(data['Social Media Links'], dict):
        for platform, link in data['Social Media Links'].items():
            print(f"{platform}: {link}")
    else:
        print(data['Social Media Links'])  # Print the error message when social media links are not found
    print("Reviews Count:", data['Reviews Count'])
    print("Reviews:")
    for review in data['Reviews']:
        print(review)
else:
    print("Failed to retrieve salon data.")