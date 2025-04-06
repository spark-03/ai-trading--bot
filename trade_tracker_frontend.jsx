import React, { useState, useEffect } from "react";
import { Table } from "@/components/ui/table";
import { Card, CardContent } from "@/components/ui/card";
import { motion } from "framer-motion";

const TradeTracker = () => {
  const [trades, setTrades] = useState([]);

  useEffect(() => {
    const fetchTrades = async () => {
      const response = await fetch("/api/trades");
      const data = await response.json();
      setTrades(data);
    };

    fetchTrades();
  }, []);

  return (
    <div className="p-6">
      <motion.h1 className="text-2xl font-bold mb-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        Paper Trades Log
      </motion.h1>
      <Card>
        <CardContent>
          <Table>
            <thead>
              <tr>
                <th>Symbol</th>
                <th>Buy Price</th>
                <th>Sell Price</th>
                <th>Profit/Loss</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {trades.map((trade, index) => (
                <tr key={index}>
                  <td>{trade.symbol}</td>
                  <td>{trade.buyPrice}</td>
                  <td>{trade.sellPrice}</td>
                  <td className={trade.profitLoss >= 0 ? "text-green-500" : "text-red-500"}>
                    {trade.profitLoss}
                  </td>
                  <td>{new Date(trade.time).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};

export default TradeTracker;
