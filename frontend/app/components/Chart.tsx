
"use client";
import { useEffect, useRef } from "react";
import { createChart, ISeriesApi } from "lightweight-charts";
export default function CandleChart({ data }: { data: any[] }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const seriesRef = useRef<ISeriesApi<"Candlestick"> | null>(null);
  const chartRef = useRef<any>(null);
  useEffect(() => {
    if (!containerRef.current) return;
    if (!chartRef.current) {
      const chart = createChart(containerRef.current, { height: 420 });
      const candleSeries = chart.addCandlestickSeries();
      seriesRef.current = candleSeries;
      chartRef.current = chart;
    }
    seriesRef.current?.setData(data);
    const resize = () => chartRef.current?.applyOptions({ width: containerRef.current?.clientWidth });
    resize(); window.addEventListener("resize", resize);
    return () => window.removeEventListener("resize", resize);
  }, [data]);
  return <div ref={containerRef} style={{ width: "100%", height: 420 }} />;
}
