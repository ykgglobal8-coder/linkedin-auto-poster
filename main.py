#!/usr/bin/env python3
"""
LinkedIn Auto Poster for Indian Business Trends
Posts daily at 9:00 AM IST
"""

import os
import json
import requests
import sys
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import google.generativeai as genai

# Configure Gemini AI
client = genai.Client(api_key=GEMINI_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

# LinkedIn credentials
LINKEDIN_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')
LINKEDIN_PERSON_URN = os.getenv('LINKEDIN_PERSON_URN')

class LinkedInAutoPoster:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        import time
import random

def fetch_with_retry(self, pytrends_method, retries=3, delay=5, *args, **kwargs):
    """Attempts an API call with retries on failure."""
    for attempt in range(retries):
        try:
            return pytrends_method(*args, **kwargs)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                wait = delay + random.uniform(0, 2)  # Add jitter
                print(f"Retrying in {wait:.1f} seconds...")
                time.sleep(wait)
            else:
                print("Max retries reached.")
                raise e  # Re-raise the final exception
    
    def get_indian_business_trends(self):
        """Get trending business topics in India using Google Trends"""
        try:
            # Import pytrends here to avoid import errors if not installed
            from pytrends.request import TrendReq
            
            # Initialize pytrends
            pytrends = TrendReq(hl='en-IN', tz=330)
            
            # Get trending searches for India
            trending_searches = pytrends.trending_searches(pn='india')
            
            # Convert to list and filter for business topics
            business_keywords = ['stock', 'market', 'business', 'economy', 
                               'finance', 'startup', 'investment', 'rupee',
                               'sensex', 'nifty', 'company', 'IPO', 'GDP',
                               'bank', 'trade', 'export', 'import', 'digital']
            
            trends = []
            for search in trending_searches[0].tolist()[:10]:  # Top 10 trends
                if any(keyword in str(search).lower() for keyword in business_keywords):
                    trends.append({
                        'title': search,
                        'traffic': 'Trending in India',
                        'articles': []
                    })
            
            return trends[:3] if trends else [{'title': 'Indian Business Trends', 'traffic': 'Daily update', 'articles': []}]
            
        except Exception as e:
            print(f"Error fetching trends with pytrends: {e}")
            
            # Fallback trends
            return [
                {'title': 'Indian Stock Market', 'traffic': 'Trending', 'articles': []},
                {'title': 'Startup Ecosystem', 'traffic': 'Growing', 'articles': []}
            ]
    
    def generate_linkedin_content(self, trend):
        """Generate LinkedIn post using Gemini AI"""
        try:
            response = client.models.generate_content(
    model='gemini-1.5-flash',  # Use a current model
    contents=prompt
)
            
            prompt = f"""Create a professional LinkedIn post about this trending Indian business topic:
            
            Trend: "{trend['title']}"
            Search Volume: {trend.get('traffic', 'High interest')}
            
            Requirements:
            1. Write an engaging caption (3-4 lines, include relevant emojis)
            2. Add 5 relevant hashtags for Indian business audience
            3. Include a thought-provoking question to encourage engagement
            4. Keep tone professional but conversational
            5. Make it suitable for LinkedIn professionals in India
            
            Format your response as valid JSON:
            {{
                "caption": "Your engaging caption here...",
                "hashtags": ["#BusinessIndia", "#Startup", "#Economy", "#Finance", "#DigitalIndia"],
                "question": "Your engaging question here?",
                "source_mention": "Based on trending searches"
            }}
            """
            
            response = model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text.strip()
            
            # Sometimes Gemini adds markdown code blocks
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].strip()
            
            content = json.loads(response_text)
            
            # Combine all parts
            full_post = f"{content['caption']}\n\n{content['question']}\n\n{' '.join(content['hashtags'])}\n\n{content.get('source_mention', '')}"
            
            return {
                'full_post': full_post,
                'trend_title': trend['title'],
                'hashtags': content['hashtags']
            }
            
        except Exception as e:
            print(f"Error generating content: {e}")
            
            # Fallback content
            return {
                'full_post': f"🚀 Trending in Indian Business: {trend['title']}\n\nWhat's your take on this development? Share your thoughts below! 👇\n\n#BusinessIndia #IndianEconomy #MarketTrends #StartupIndia #DigitalGrowth\n\nBased on trending searches",
                'trend_title': trend['title'],
                'hashtags': ['#BusinessIndia', '#IndianEconomy', '#MarketTrends', '#StartupIndia', '#DigitalGrowth']
            }
    
    def create_business_meme(self, trend_title, quote):
        """Create a professional-looking meme for LinkedIn"""
        try:
            # Create image with LinkedIn blue theme
            width, height = 1200, 627  # LinkedIn recommended size
            
            # Create gradient background
            img = Image.new('RGB', (width, height), color='#0077b5')
            draw = ImageDraw.Draw(img)
            
            # Try to load font, fallback to default
            try:
                title_font = ImageFont.truetype("arial.ttf", 64)
                quote_font = ImageFont.truetype("arial.ttf", 48)
            except:
                # Use default font
                title_font = ImageFont.load_default()
                quote_font = ImageFont.load_default()
            
            # Add title
            title_text = f"🔥 TRENDING: {trend_title[:40]}{'...' if len(trend_title) > 40 else ''}"
            title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            
            draw.text((title_x, 100), title_text, fill='white', font=title_font, stroke_width=2, stroke_fill='#004471')
            
            # Add quote
            lines = []
            words = quote.split()
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                bbox = draw.textbbox((0, 0), test_line, font=quote_font)
                test_width = bbox[2] - bbox[0]
                
                if test_width < width - 200:  # 100px margin on each side
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw each line
            for i, line in enumerate(lines[:3]):  # Max 3 lines
                bbox = draw.textbbox((0, 0), line, font=quote_font)
                line_width = bbox[2] - bbox[0]
                line_x = (width - line_width) // 2
                draw.text((line_x, 250 + (i * 80)), line, fill='#f0f0f0', font=quote_font)
            
            # Add footer
            draw.text((width - 300, height - 50), "#BusinessTrendsIndia", fill='#cccccc', font=quote_font)
            
            # Save to bytes
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG', quality=95)
            img_bytes = img_byte_arr.getvalue()
            
            return img_bytes
            
        except Exception as e:
            print(f"Error creating image: {e}")
            # Return simple colored image as fallback
            img = Image.new('RGB', (1200, 627), color='#0077b5')
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            return img_byte_arr.getvalue()
    
    def upload_image_to_linkedin(self, image_bytes):
        """Upload image to LinkedIn and get URN"""
        try:
            # Step 1: Initialize upload
            init_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
            init_payload = {
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": f"urn:li:person:{LINKEDIN_PERSON_URN}",
                    "serviceRelationships": [{
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }]
                }
            }
            
            headers = {
                "Authorization": f"Bearer {LINKEDIN_TOKEN}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            
            init_response = requests.post(init_url, json=init_payload, headers=headers)
            
            if init_response.status_code == 200:
                init_data = init_response.json()
                upload_url = init_data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
                asset_urn = init_data['value']['asset']
                
                # Step 2: Upload image
                upload_headers = {
                    "Authorization": f"Bearer {LINKEDIN_TOKEN}"
                }
                
                upload_response = requests.put(
                    upload_url,
                    data=image_bytes,
                    headers=upload_headers
                )
                
                if upload_response.status_code in [200, 201]:
                    return asset_urn
                else:
                    print(f"Image upload failed: {upload_response.status_code} - {upload_response.text}")
            else:
                print(f"Upload initialization failed: {init_response.status_code} - {init_response.text}")
                
        except Exception as e:
            print(f"Error uploading image: {e}")
        
        return None
    
    def post_to_linkedin(self, content, image_urn):
        """Create post on LinkedIn with image"""
        try:
            url = "https://api.linkedin.com/v2/ugcPosts"
            
            payload = {
                "author": f"urn:li:person:{LINKEDIN_PERSON_URN}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": content['full_post']
                        },
                        "shareMediaCategory": "IMAGE",
                        "media": [
                            {
                                "status": "READY",
                                "description": {
                                    "text": f"Business Trend: {content['trend_title'][:200]}"
                                },
                                "media": image_urn
                            }
                        ]
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            headers = {
                "Authorization": f"Bearer {LINKEDIN_TOKEN}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 201:
                print(f"✅ Post published successfully!")
                print(f"📝 Preview: {content['full_post'][:100]}...")
                return True
            else:
                print(f"❌ Post failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"Error posting to LinkedIn: {e}")
            return False
    
    def run(self):
        """Main execution function"""
        print("=" * 50)
        print(f"LinkedIn Auto Poster - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        # 1. Get trending topics
        print("\n📊 Fetching Indian business trends...")
        trends = self.get_indian_business_trends()
        
        if not trends:
            print("❌ No trends found. Exiting.")
            return False
        
        selected_trend = trends[0]
        print(f"✅ Selected trend: {selected_trend['title']}")
        print(f"   Search volume: {selected_trend.get('traffic', 'N/A')}")
        
        # 2. Generate content
        print("\n🤖 Generating LinkedIn content...")
        content = self.generate_linkedin_content(selected_trend)
        print(f"✅ Content generated: {len(content['full_post'])} characters")
        
        # 3. Create meme/image
        print("\n🎨 Creating business meme...")
        meme_quote = content['full_post'].split('\n')[0]  # Use first line as quote
        image_bytes = self.create_business_meme(selected_trend['title'], meme_quote)
        print(f"✅ Image created: {len(image_bytes)} bytes")
        
        # 4. Upload image to LinkedIn
        print("\n⬆️ Uploading image to LinkedIn...")
        image_urn = self.upload_image_to_linkedin(image_bytes)
        
        if not image_urn:
            print("⚠️ Image upload failed. Posting without image...")
        
        # 5. Post to LinkedIn
        print("\n🚀 Posting to LinkedIn...")
        success = self.post_to_linkedin(content, image_urn)
        
        print("\n" + "=" * 50)
        print(f"Process completed: {'SUCCESS' if success else 'FAILED'}")
        print("=" * 50)
        
        return success

def main():
    """Entry point"""
    # Validate environment variables
    required_env_vars = ['GEMINI_API_KEY', 'LINKEDIN_ACCESS_TOKEN', 'LINKEDIN_PERSON_URN']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please add them to GitHub Secrets")
        sys.exit(1)
    
    # Run the poster
    poster = LinkedInAutoPoster()
    success = poster.run()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
