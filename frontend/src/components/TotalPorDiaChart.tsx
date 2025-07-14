import React from 'react';
import ReactECharts from 'echarts-for-react';
import { useQuery } from '@tanstack/react-query';
import { fetchWithAuth } from '../hooks/useCompras'; // Usando a função que criamos anteriormente

// Define o tipo de dado que esperamos da nossa API
interface DadosGrafico {
  data: string;  // Formato 'AAAA-MM-DD'
  total: number;
}

/**
 * Gera as opções de configuração para o gráfico ECharts.
 * @param data Os dados recebidos da API.
 * @returns Um objeto de configuração para o ECharts.
 */
const getChartOptions = (data: DadosGrafico[]) => {
  return {
    // Tooltip que aparece ao passar o mouse
    title: {
          text: "titulo",
          left: 'center',
        },
        tooltip: {
          trigger: 'axis', // O tooltip aparecerá ao passar o mouse sobre o eixo
          axisPointer: {
            type: 'shadow', // O ponteiro será uma sombra sobre a barra
          },
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true,
        },
        xAxis: [
          {
            type: 'category', // Eixo de categorias (dias)
            axisTick: {
              alignWithLabel: true,
            },
          },
        ],
        yAxis: [
          {
            type: 'value', // Eixo de valores (total)
          },
        ],
        series: [
          {
            name: 'Total',
            type: 'bar', // TIPO DE GRÁFICO: BARRAS
            barWidth: '60%',
            itemStyle: {
              color: '#5470C6' // Cor das barras
            },
            emphasis: {
                focus: 'series'
            }
          },
        ],
        // Habilita a funcionalidade de zoom e arrastar
        dataZoom: [
            {
                type: 'inside',
                start: 0,
                end: 100
            },
            {
                start: 0,
                end: 100
            }
        ]
      };
};

/**
 * Componente de dashboard que exibe um gráfico de Donut
 * mostrando a quantidade de usuários por tipo.
 */
export default function TotalDiaDashboard() {

  const { data, isLoading, isError, error } = useQuery<DadosGrafico[]>({
    queryKey: ['dashboardTotalDias'], // Chave única para esta query
    queryFn: async () => {
      const response = await fetchWithAuth('/dashboard/total/compras');

      if (!response.ok) {
        throw new Error('Falha ao carregar os dados do dashboard.');
      }
      return response.json();
    }
  });

  if (isLoading) {
    return (
      <div className="p-4 bg-white rounded-lg shadow-md h-96 flex items-center justify-center">
        <p className="text-gray-500">Carregando dados do gráfico...</p>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="p-4 bg-white rounded-lg shadow-md h-96 flex items-center justify-center">
        <p className="text-red-500">Erro: {error.message}</p>
      </div>
    );
  }

  return (
    <div className="p-4 bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-2 text-gray-700">Total de compras por dia</h2>
      <ReactECharts
        option={getChartOptions(data || [])}
        style={{ height: '400px', width: '100%' }}
        notMerge={true}
        lazyUpdate={true}
      />
    </div>
  );
}