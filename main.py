import requests
import dns.resolver
import whois
from bs4 import BeautifulSoup

def get_website_info(url):
    print(f"Gathering information for: {url}\n")
    
    # Ensure we're only passing the domain, not the full URL
    domain = url.split("//")[-1].split("/")[0]  # Remove 'http://' or 'https://' and path
    
    # WHOIS Information
    try:
        w = whois.whois(domain)
        print("WHOIS Information:")
        print(f"Domain Name: {w.domain_name}")
        print(f"Registrar: {w.registrar}")
        print(f"Creation Date: {w.creation_date}")
        print(f"Expiration Date: {w.expiration_date}")
        print(f"Name Servers: {w.name_servers}\n")
    except Exception as e:
        print(f"Error fetching WHOIS data: {e}\n")

    # DNS Records
    try:
        print("DNS Records:")
        answers = dns.resolver.resolve(domain, 'A')  # 'A' record for IPv4 address
        for rdata in answers:
            print(f"IP Address: {rdata}")
        print()
    except Exception as e:
        print(f"Error fetching DNS records: {e}\n")

    # Fetching Website Metadata

    try:
        # Try both HTTP and HTTPS
        for scheme in ['http', 'https']:
            try:
                response = requests.get(f"{scheme}://{domain}")
                response.raise_for_status()  # Raise an error for bad status codes (e.g., 404)
                
                # Parse the content of the page
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract metadata
                title = soup.title.string if soup.title else 'No title found'
                description = soup.find('meta', attrs={'name': 'description'})
                description_content = description['content'] if description else 'No description found'
                
                keywords = soup.find('meta', attrs={'name': 'keywords'})
                keywords_content = keywords['content'] if keywords else 'No keywords found'
                
                # Print the metadata
                print("Website Metadata:")
                print(f"Title: {title}")
                print(f"Description: {description_content}")
                print(f"Keywords: {keywords_content}\n")
                return  # If the website was fetched successfully, exit the loop
                
            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch {scheme}://{domain}: {e}")
                continue  # Try the next scheme (http/https)
        print(f"Could not fetch website metadata for {domain}.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    target_url = input("Enter the website URL (without http/https): ").strip()
    get_website_info(target_url)
