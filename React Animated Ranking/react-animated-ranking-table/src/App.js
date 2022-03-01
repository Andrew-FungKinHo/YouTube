import React from 'react';
import {useState,useEffect} from 'react';
import {Reorder} from 'framer-motion'

// reorder
function App() {
  const [cryptoData,setCryptoData] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      fetchCryptoData();
      console.log('Table Updated');
    },5000)
    return () => clearInterval(interval);
  },[cryptoData])

  const fetchCryptoData = async () => {
    const data = await fetch('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd');
    const apiResponse = await data.json();
    const sortedData = apiResponse.sort((a,b) => b.price_change_percentage_24h - a.price_change_percentage_24h)
    // console.log(sortedData);
    setCryptoData(sortedData)
  }

  return (
    <div className="container mx-auto px-4 sm:px-8">
      <div className="py-8">
        <div>
          <h2 className="text-2xl font-semibold leading-tight">React real-time animated ranking table for Cryptocurrencies</h2>
        </div>
        <div className="-mx-4 sm:-mx-8 px-4 sm:px-8 py-4 overflow-x-auto">
          <div
            className="inline-block min-w-full shadow-md rounded-lg overflow-hidden"
          >
            <Reorder.Group values={cryptoData} onReorder={setCryptoData}>
            <table className="min-w-full leading-normal">
              <thead>
                <tr>
                  <th
                    className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider"
                  >
                    Cryptocurrency
                  </th>
                  <th
                    className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider"
                  >
                    Price
                  </th>
                  <th
                    className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider"
                  >
                    Market Cap
                  </th>
                  <th
                    className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider"
                  >
                    Total Volume 
                  </th>
                  <th
                    className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider"
                  >
                    Price Change 24h 
                  </th>
                  <th
                    className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider"
                  >
                    Price Percentage 24h 
                  </th>
                  <th
                    className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider"
                  >
                    Price Trend
                  </th>
                </tr>
              </thead>
              <tbody>
                {cryptoData.map(cryptocurrency => 
                <Reorder.Item as='tr' key={cryptocurrency.price_change_percentage_24h} value={cryptocurrency.price_change_percentage_24h}>
                  <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                    <div className="flex">
                      <div className="flex-shrink-0 w-10 h-10">
                        <img
                          className="w-full h-full rounded-full"
                          src={cryptocurrency.image}
                          alt=""
                        />
                      </div>
                      <div className="ml-3">
                        <p className="text-gray-900 whitespace-no-wrap">
                          {cryptocurrency.name}
                        </p>
                        <p className="text-gray-600 whitespace-no-wrap">{cryptocurrency.symbol}</p>
                      </div>
                    </div>
                  </td>
                  <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                    <p className="text-gray-900 whitespace-no-wrap">${cryptocurrency.current_price}</p>
                    <p className="text-gray-600 whitespace-no-wrap">USD</p>
                  </td>
                  <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                    <p className="text-gray-600 whitespace-no-wrap">{cryptocurrency.market_cap}</p>
                  </td>
                  <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                    <p className="text-gray-600 whitespace-no-wrap">{cryptocurrency.total_volume}</p>
                  </td>
                  <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                    <p className="text-gray-600 whitespace-no-wrap">${cryptocurrency.price_change_24h}</p>
                  </td>
                  <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                    <p className="text-gray-600 whitespace-no-wrap">{cryptocurrency.price_change_percentage_24h}%</p>
                  </td>
                  {cryptocurrency.price_change_percentage_24h > 0 ? 
                  (<td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                    <span
                      className="relative inline-block px-3 py-1 font-semibold text-green-900 leading-tight"
                    >
                      <span
                        aria-hidden
                        className="absolute inset-0 bg-green-200 opacity-50 rounded-full"
                      ></span>
                      <span className="relative">Upward Trend</span>
                    </span>
                  </td>) 
                  : 
                  (<td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                    <span
                      className="relative inline-block px-3 py-1 font-semibold text-red-900 leading-tight"
                    >
                      <span
                        aria-hidden
                        className="absolute inset-0 bg-red-200 opacity-50 rounded-full"
                      ></span>
                      <span className="relative">Downward Trend</span>
                    </span>
                  </td>
                  )}
                </Reorder.Item>
                )}
              </tbody>
            </table>
            </Reorder.Group>
            
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;