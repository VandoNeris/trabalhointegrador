

import React from 'react';
import ReactECharts from 'echarts-for-react';
import { EChartsOption } from 'echarts';

export interface DadosGraficoTotalDia {
  data: string;  // Formato 'AAAA-MM-DD'
  total: number;
}

interface TotalPorDiaChartProps {
  dados: DadosGraficoTotalDia[];
  titulo?: string;
  isLoading?: boolean;
}

const TotalPorDiaChart: React.FC<TotalPorDiaChartProps> = ({ dados, titulo = "Total por Dia", isLoading }) => {
  const getChartOptions = (chartData: DadosGraficoTotalDia[]): EChartsOption => {
    // Separa as datas e os totais para os eixos do gráfico
    const datas = chartData.map(item => item.data);
    const totais = chartData.map(item => item.total);

    return {
      title: {
        text: titulo,
        left: 'center',
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
      },
      grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
      xAxis: [{
        type: 'category',
        data: datas, // <-- PREENCHENDO O EIXO X
        axisTick: { alignWithLabel: true },
      }],
      yAxis: [{ type: 'value' }],
      series: [{
        name: 'Total',
        type: 'bar',
        barWidth: '60%',
        data: totais, // <-- PREENCHENDO AS BARRAS (SÉRIE)
        itemStyle: { color: '#5470C6' },
      }],
      dataZoom: [{ type: 'inside' }, {}],
    };
  };

  if (isLoading) {
    return (
      <div className="p-4 bg-white rounded-lg shadow-md h-96 flex items-center justify-center">
        <p className="text-gray-500">Carregando dados do gráfico...</p>
      </div>
    );
  }

  return (
    <div className="p-4 bg-white rounded-lg shadow-md">
      <ReactECharts
        option={getChartOptions(dados || [])} // Garante que nunca seja undefined
        style={{ height: '400px', width: '100%' }}
        notMerge={true}
        lazyUpdate={true}
      />
    </div>
  );
}

export default TotalPorDiaChart;