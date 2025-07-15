# 🌐 Advanced Domain Name Generator

An intelligent domain name generator that combines AI-powered suggestions with systematic domain availability checking.

## ✨ Features

- 🤖 **AI-Powered Generation**: Uses OpenRouter API with Gemini 2.5 Flash to generate contextual domain suggestions
- 🔍 **Dual Verification**: DNS + WHOIS checking for accurate availability detection
- 🎯 **Custom Words**: Add your own words and partial stems
- 🚀 **Startup-Style Endings**: Modern domain endings (ly, io, ai, etc.)
- 🔗 **GoDaddy Integration**: Direct links to check and register domains
- 📈 **Batch Processing**: Check multiple domains simultaneously
- 🎨 **Beautiful CLI**: Intuitive command-line interface with progress indicators
- 🔄 **Continuous Generation**: Keep generating new domains until you find the perfect one

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/victoriano/domain-generator.git
cd domain-generator

# Install dependencies using uv
uv sync

# Set up OpenRouter API key (optional, for AI features)
export OPENROUTER_API_KEY="your-api-key-here"
# Or create a .env file with: OPENROUTER_API_KEY=your-api-key-here
```

### Usage

```bash
# Run the generator
uv run domain_generator.py

# Or with Python directly
python domain_generator.py
```

## 🔧 Setup AI Features

1. Get your API key from [OpenRouter](https://openrouter.ai/keys)
2. Set the environment variable:
   ```bash
   export OPENROUTER_API_KEY="sk-or-v1-your-key-here"
   ```
3. Or create a `.env` file:
   ```
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   ```

## 🎯 Example Usage

Perfect for generating domains for:
- **SaaS Applications**: "project management tool for startups"
- **E-commerce**: "sustainable fashion marketplace"
- **AI/ML Projects**: "chatgpt vertical for SEO research data analysis"
- **Health Tech**: "telemedicine platform for rural areas"
- **FinTech**: "cryptocurrency trading dashboard"

## 🔄 Workflow Features

- **Continuous Generation**: After each session, choose to generate more domains
- **AI Context**: Describe your business for tailored domain suggestions
- **Custom Words**: Add your specific keywords
- **Partial Words**: Use word stems like 'octo', 'meta', 'zen'
- **Compulsory Words**: Ensure specific terms appear in all domains
- **Startup Endings**: Toggle modern suffixes (ly, io, ai, app, hub, etc.)

## 🔍 Verification Methods

- **DNS Lookup**: Fast initial screening
- **WHOIS Verification**: Detailed availability confirmation
- **Real-time Checking**: Up-to-date domain status
- **Batch Processing**: Efficient bulk verification

## 🛠️ Technical Details

- **Language**: Python 3.13+
- **AI Model**: Google Gemini 2.5 Flash (via OpenRouter)
- **Dependencies**: requests, python-dotenv
- **Package Manager**: uv (modern Python package manager)

## 📝 Configuration Options

- **Custom Words**: Add industry-specific terms
- **Partial Words**: Use word stems and fragments  
- **Compulsory Words**: Ensure specific terms appear in all domains
- **Startup Endings**: Modern domain suffixes (ly, io, ai, etc.)
- **Number Integration**: Include numbers in domain names

## 🎨 Output Features

- **Verification Icons**: 🔍 WHOIS verified, 📡 DNS only
- **Source Indicators**: 🤖 AI generated, 🔧 Manual combination
- **Progress Tracking**: Real-time availability checking progress
- **GoDaddy Links**: Direct registration links for available domains
- **Organized Results**: Separate available/taken domain lists

## 📈 Performance

- **Batch Processing**: Check 50+ domains simultaneously
- **Intelligent Delays**: Respectful API usage with rate limiting
- **Error Handling**: Graceful handling of network issues
- **Progress Indicators**: Real-time feedback during processing

## 🔒 Security

- **API Key Protection**: Environment variables and .env file support
- **.gitignore**: Prevents sensitive information from being committed
- **No Data Storage**: No persistence of API keys or personal data

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

- Create an issue for bugs or feature requests
- Check out the [OpenRouter documentation](https://openrouter.ai/docs) for API details
- Visit [GoDaddy](https://www.godaddy.com) for domain registration

---

**Made with ❤️ for entrepreneurs and developers looking for the perfect domain name.**
