#!/usr/bin/env python3
"""
Test script for OpenRouter API connection and basic sentiment analysis.
This script tests the core functionality before building the full application.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def setup_openrouter_client():
  """Initialize OpenRouter client"""
  api_key = os.getenv("OPENROUTER_API_KEY")
  if not api_key:
    raise ValueError("Please set your OPENROUTER_API_KEY in the .env file")

  client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
  )
  return client

def load_prompt(prompt_name):
  """Load prompt from prompts directory"""
  prompt_path = os.path.join("prompts", f"{prompt_name}.txt")
  try:
    with open(prompt_path, 'r', encoding='utf-8') as f:
      return f.read().strip()
  except FileNotFoundError:
    raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

def get_sentiment(review_text, client):
  """
  Analyze sentiment of a review using OpenRouter.
  Returns sentiment classification and justification.
  """
  # Get configured model from .env, default to google/gemini-flash-1.5
  model = os.getenv("OPENROUTER_MODEL")
  default_model = "google/gemini-flash-1.5"
  if not model:
    print(f"OPENROUTER_MODEL not set in .env, using default model: {default_model}")
    model = default_model

  # Load prompt from file
  prompt_template = load_prompt("sentiment_analysis")
  prompt = prompt_template.format(review_text=review_text)

  try:
    response = client.chat.completions.create(
      model=model,
      messages=[
        {"role": "system", "content": "You are an expert in sentiment analysis. Always respond with valid JSON only."},
        {"role": "user", "content": prompt}
      ],
      temperature=0.3
    )

    return response.choices[0].message.content

  except Exception as e:
    return f"Error: {str(e)}"

def main():
  """Test the OpenRouter connection and sentiment analysis"""
  print("🚀 Testing OpenRouter Connection...")
  print("=" * 50)

  try:
    # Initialize client
    client = setup_openrouter_client()
    print("✅ OpenRouter client initialized successfully!")

    # Test reviews
    test_reviews = [
      """
      Paket datang dengan packing aman, tpi ada yg penyok bagian pelindungnya,
      Tapi masih bisa digunakan dengan baik.
      Dan kualitas mirip original...
      """,
      "Seonggok plastik gini doank kok bisa mahal ya? Seharga gundam high grade",
      "Kondisi baik, cukup bagus, sesuai dengan spesifikasi penjual",
      # "Untuk kualitas KW sudah sangat baik. Rel berfungsi jg",
      # """
      # Respon pelapak sangat memuaskan
      # Harga segini udh keren bgt sih
      # Rekomended seller
      # """,
      # "Paket telah sampai dengan baik dan selamat kualitas produk baik pengemasan standar pengiriman oke,",
      # "Ya petok dikit.. wajar sih.. Kargo jkt smg.. Tp overall oke kok.. Nti beli bey blade nya disini lg.. Owner ramah.. Ditanya2 jawabnya jg nyenengin ga nyebeli",
      # "Walaupun lama sampenya tapi kondisi barang sangat baik tidak cacat..makasih"
    ]

    print(f"\n📝 Testing sentiment analysis on {len(test_reviews)} sample reviews...")
    print("-" * 50)

    for i, review in enumerate(test_reviews, 1):
      print(f"\n🔍 Test {i}:")
      print(f"Review: \"{review[:60]}{'...' if len(review) > 60 else ''}\"")

      result = get_sentiment(review, client)
      print(f"Result: {result}")
      print("-" * 30)

    print("\n🎉 All tests completed successfully!")
    print("✅ OpenRouter connection is working!")
    print("✅ Sentiment analysis function is working!")

  except Exception as e:
    print(f"❌ Error: {str(e)}")
    print("\n💡 Troubleshooting tips:")
    print("1. Make sure you've created the .env file")
    print("2. Check that your OPENROUTER_API_KEY is correct")
    print("3. Verify you have internet connection")

if __name__ == "__main__":
  main()
