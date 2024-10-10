import requests
from collections import Counter

# GitHub token for authentication
GITHUB_TOKEN = INSERT_TOKEN_HERE

# Function to search GitHub repositories based on the hardware product
def search_github_repos(hardware_product, per_page=100):
    query = f"{hardware_product}"
    all_repos = []
    page = 1
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    
    while True:
        # Make the request to GitHub API with pagination
        url = f"https://api.github.com/search/repositories?q={query}&per_page={per_page}&page={page}"
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            repos = data.get('items', [])
            if not repos:  # If no more repositories are found, break the loop
                break
            all_repos.extend(repos)
            page += 1  # Move to the next page
        else:
            print(f"Failed to fetch data: {response.status_code}")
            break
    
    return all_repos

# Function to count the popularity of programming languages
def get_top_languages(repos, top_n=5):
    language_counter = Counter()
    
    # Count the occurrences of each programming language
    for repo in repos:
        language = repo.get('language')
        if language:
            language_counter[language] += 1
    
    # Return the top_n most common languages (sorted by frequency)
    return [language for language, _ in language_counter.most_common(top_n)]

# Function to search GitHub repositories with the top 5 languages for each hardware
def search_github_repos_with_top_languages(hardware_product, top_languages, per_page=100):
    language_query = '+'.join([f'language:{lang}' for lang in top_languages])
    query = f"{hardware_product}+{language_query}"
    
    all_repos = []
    page = 1
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    
    while True:
        # Make the request to GitHub API with pagination
        url = f"https://api.github.com/search/repositories?q={query}&per_page={per_page}&page={page}"
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            repos = data.get('items', [])
            if not repos:  # If no more repositories are found, break the loop
                break
            all_repos.extend(repos)
            page += 1  # Move to the next page
        else:
            print(f"Failed to fetch data: {response.status_code}")
            break
    
    return all_repos

# Main function to analyze repositories and filter by top 5 languages
def analyze_hardware_repos_with_top_languages(hardware_products):
    for product in hardware_products:
        print(f"Analyzing repositories related to {product}...")

        # Step 1: Search repositories related to the hardware
        repos = search_github_repos(product)

        # Step 2: Get the top 5 languages for the hardware product
        top_languages = get_top_languages(repos)
        print(f"Top 5 languages for {product}: {top_languages}")
        
        # Step 3: Search repositories using top 5 languages as filters
        filtered_repos = search_github_repos_with_top_languages(product, top_languages)
        
        # Print the count of repositories found with top languages
        print(f"Found {len(filtered_repos)} repositories for {product} with top 5 languages.\n")

# Main script
if __name__ == "__main__":
    # List of hardware products you want to analyze
    hardware_products = ['Flipper Zero', 'WiFi Pineapple', 'HackRF']
    
    # Analyze the repositories and filter using top 5 languages
    analyze_hardware_repos_with_top_languages(hardware_products)