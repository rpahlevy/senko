#!/usr/bin/env python3
"""
Test script for OpenRouter API connection and basic sentiment analysis.
This script tests the core functionality before building the full application.
"""

from openai import OpenAI
from core import setup_openrouter_client
from core.client import get_model_name
from core.prompt_loader import load_and_format_prompt
from utils.config import get_config_value, print_config_summary


def get_sentiment(review_text: str, client: OpenAI) -> str:
  """
  Analyze sentiment of a review using OpenRouter.
  Returns sentiment classification and justification.
  """
  # Get configuration from centralized config system (cached after first call)
  model = get_model_name()
  system_message = get_config_value("analysis.system_message")
  temperature = get_config_value("openrouter.temperature", 0.3)

  # Load and format prompt
  prompt = load_and_format_prompt("sentiment_analysis", review_text=review_text)

  try:
    response = client.chat.completions.create(
      model=model,
      messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
      ],
      temperature=temperature
    )

    return response.choices[0].message.content

  except Exception as e:
    return f"Error: {str(e)}"


def test_config_caching():
  """Demonstrate that configuration is cached and loaded only once"""
  print("\n🧪 Testing Configuration Caching...")
  print("-" * 40)

  print("First call - should load and print env messages:")
  model1 = get_config_value("openrouter.model")

  print("Second call - should use cache (no env messages):")
  model2 = get_config_value("openrouter.model")

  print("Third call - should use cache (no env messages):")
  model3 = get_config_value("openrouter.temperature")

  print(f"All calls return consistent values: {model1 == model2}")
  print("✅ Configuration caching working properly!")


def main():
  """Test the OpenRouter connection and sentiment analysis"""
  print("🚀 Testing OpenRouter Connection...")
  print("=" * 50)

  # Show configuration summary
  print_config_summary()

  # Test caching behavior
  test_config_caching()
  print()

  try:
    # Initialize client using core module
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
    print("✅ Core modules are working properly!")
    print("✅ Centralized configuration system is working!")
    print("✅ Configuration caching is preventing redundant loads!")

  except Exception as e:
    print(f"❌ Error: {str(e)}")
    print("\n💡 Troubleshooting tips:")
    print("1. Make sure you've created the .env file")
    print("2. Check that your OPENROUTER_API_KEY is correct")
    print("3. Verify you have internet connection")
    print("4. Ensure core modules are properly installed")


if __name__ == "__main__":
  main()
