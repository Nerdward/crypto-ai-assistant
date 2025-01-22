# Web3 Crypto AI Assistant

An AI-powered assistant for analyzing and optimizing cryptocurrency portfolios using real-time market data and historical analysis.

## Project Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd web3-crypto-ai-assistant
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Set up environment variables in `.env`:
```bash
OPENAI_API_KEY=your_openai_key
INFURA_API=your_infura_api_key
WALLET_ADDRESS=your_ethereum_wallet
ETHERSCAN_API_KEY=your_etherscan_key
```

4. Run the FastAPI server:
```bash
uvicorn src.main:app --reload
```

## Architecture Overview

### Core Components

- **Agent**: Central component that orchestrates interactions between the LLM and tools
- **Tools**: Collection of utilities for data fetching and analysis:
  - Portfolio management (balances, distribution)
  - Historical data retrieval
  - Market trend analysis
  - Price tracking
  - Visualization generation

### Data Flow

1. User query → FastAPI endpoint
2. Agent processes query using LangChain
3. Tools fetch data from:
   - CoinGecko API (market data)
   - Ethereum blockchain (wallet data)
   - Etherscan API (transaction history)
4. Response generation with analysis and visualizations

## API Documentation

### Endpoint: `/ask-the-ai-agent`

**Method**: GET

**Query Parameters**:
- `query`: String containing user's question or command

**Example Request**:
```bash
curl "http://localhost:8000/ask-the-ai-agent?query=Show%20my%20portfolio%20distribution"
```

**Response**: JSON object containing agent's analysis and recommendations

## Technologies Used

- **Framework**: FastAPI
- **Blockchain Integration**: Web3.py
- **AI/ML**: 
  - LangChain
  - OpenAI GPT-4
- **Data Analysis**: 
  - Pandas
  - NumPy
  - Matplotlib
- **Package Management**: Poetry
- **APIs**:
  - CoinGecko
  - Etherscan
  - Infura

## Future Improvements

1. **Technical Enhancements**
   - Implement caching for API calls
   - Add support for more blockchains
   - Integrate DEX price feeds
   - Implement WebSocket for real-time updates

2. **Features**
   - Portfolio rebalancing suggestions
   - Risk assessment metrics
   - Tax reporting integration
   - Custom alert system
   - Multi-wallet support

3. **Security**
   - Rate limiting
   - API key rotation
   - Input validation enhancement
   - Wallet signature verification

4. **Documentation**
   - API swagger documentation
   - Interactive examples
   - Testing documentation
   - Deployment guides