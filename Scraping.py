import requests
from bs4 import BeautifulSoup
import re

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
        parent_div = soup.select_one('#pageSection > div:nth-child(6) > div')

        # Find all the service items within the parent div
        service_items = parent_div.select('ul > li > div > ul:nth-child(1) > li')

        # Iterate over each service item to extract service name and price
        services = []
        for item in service_items:
            service_name = item.find('h3', {'data-testid': 'service-name'}).get_text(strip=True)
            service_price = item.find('div', {'data-testid': 'service-price'}).get_text(strip=True)
            services.append({'Service': service_name, 'Price': service_price})

        
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


        
        # Extract reviews count and average rating
        review_div = soup.find("div", class_="purify_VXAITtHvgDHJSpiutS+aCQ==")
        review_count_text = review_div.find("div", class_="purify_aNo2rKM2GaqragdL24RFJA==").text
        review_count = int(re.search(r'\d+', review_count_text).group())
        average_rating_text = review_div.find("div", class_="purify_lZvWIWxIpgyX2b3dr9or0A==").text
        average_rating = float(re.search(r'\d+\.\d+', average_rating_text).group())
        
        # Find and extract individual review ratings

        # Extract all reviews
        review_items = soup.find_all('div', {'data-testid': 'review-item'})

        reviews = []
        for item in review_items:
            # Extract reviewer name
            reviewer_and_date_div = soup.find('div', {'class': 'purify_vWHLz7KKXvW-ACHxCe5XkQ=='})
        
            # Extract reviewer name
            reviewer_name_element = reviewer_and_date_div.find('span', {'class': 'purify_HRlYZ9s5U73L+xgNWotErg=='})
            reviewer_name = reviewer_name_element.text.strip() if reviewer_name_element else "Reviewer name not found"

            # Extract review date
            review_date_element = reviewer_and_date_div.find('span', {'class': 'purify_VsjLagY8Ojq+9Ze+lWDQGQ=='})
            review_date = review_date_element.text.strip() if review_date_element else "Review date not found"

            
            # Extract review text
            review_text_element = item.find('div', {'class': 'purify_1KV69VGQK1FO5206zDXt6w=='})
            review_text = review_text_element.text.strip() if review_text_element else "Review text not found"

            # Extract service name
            service_name_element = item.find('span', {'data-testid': 'review-service'})
            service_name = service_name_element.text.strip() if service_name_element else "Service name not found"

            # Extract staffer name
            staffer_name_element = item.find('span', {'data-testid': 'review-staffer'})
            staffer_name = staffer_name_element.text.strip() if staffer_name_element else "Staffer name not found"

            reviews.append({
                'Reviewer': reviewer_name,
                'Date': review_date,
                'Review': review_text,
                'Service': service_name,
                'Staffer': staffer_name
            })


    
            
        # Create dictionary to store all the data
        salon_data = {
            'Salon Name': salon_name,
            'Location': location,
            'Services': services,
            'Salon Work Images': images,
            'Phone Number': phone_number,
            'Work Hours': work_days_and_hours,
            'Social Media Links': social_media_links,
            'Reviews Count': review_count,
            'Average Rating': average_rating,
            'Reviews': reviews,
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
    print("Services:")
    for service in data['Services']:
        print(f"  - {service['Service']}: {service['Price']}")
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
    print("Average Rating:", data['Average Rating'])
    print("Reviews:")
    for idx, review in enumerate(data['Reviews']):
        print(f"Review {idx+1}:")
        print(f"Reviewer: {review['Reviewer']}")
        print(f"Date: {review['Date']}")
        print(f"Review: {review['Review']}")
        print(f"Service: {review['Service']}")
        print(f"Staffer: {review['Staffer']}")
        print()
else:
    print("Failed to retrieve salon data.")
