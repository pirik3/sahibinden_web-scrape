- Use a proxy or VPN to bypass bot detection mechanisms.
  - Note: Cloudflare protection may still block some scraping attempts. Additional measures (like headless browser spoofing or delay tactics) may be required.
    
- Listings are typically limited to 20 pages, with 50 listings per page, allowing a maximum of ~1000 listings per scan.
- To work around this limitation:
  - Divide scans using filters such as by city, or even more granularly by town.
  - Loop through each filter to ensure all listings are scanned.
    
- To track price changes directly on the website, a browser extension can be added.
  
- Inject a script to display price history inside the element with the class; "classified-price-container"
