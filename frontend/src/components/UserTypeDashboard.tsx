import React from 'react';
import ReactECharts from 'echarts-for-react';
import { useQuery } from '@tanstack/react-query';
import { fetchWithAuth } from '../hooks/usePessoas'; // Usando a função que criamos anteriormente

// Define o tipo de dado que esperamos da nossa API
interface UserTypeData {
  value: number;
  name: string;
  tipo: number;
}

/**
 * Gera as opções de configuração para o gráfico ECharts.
 * @param data Os dados recebidos da API.
 * @returns Um objeto de configuração para o ECharts.
 */
const getChartOptions = (data: UserTypeData[]) => {
  return {
    // Tooltip que aparece ao passar o mouse
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)' // Formato: Nome: Valor (Porcentagem%)
    },
    // Legenda do gráfico
    legend: {
      top: '5%',
      left: 'center'
    },
    // A série de dados do gráfico
    series: [
      {
        name: 'Usuários por Tipo',
        type: 'pie', // Tipo do gráfico
        radius: ['40%', '70%'], // Raio interno e externo, o que cria o efeito "Donut"
        avoidLabelOverlap: false,
        padAngle: 5,
        itemStyle: {
          borderRadius: 10
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 30,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: data, // Injecta os dados da API aqui!
      },
    ],
  };
};

/**
 * Componente de dashboard que exibe um gráfico de Donut
 * mostrando a quantidade de usuários por tipo.
 */
export default function UserTypeDashboard() {

  const { data, isLoading, isError, error } = useQuery<UserTypeData[]>({
    queryKey: ['dashboardUserTypes'], // Chave única para esta query
    queryFn: async () => {
      const response = await fetchWithAuth('/dashboard/users/type');

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
      <h2 className="text-xl font-semibold mb-2 text-gray-700">Usuários por Tipo</h2>
      <ReactECharts
        option={getChartOptions(data || [])}
        style={{ height: '400px', width: '100%' }}
        notMerge={true}
        lazyUpdate={true}
      />
    </div>
  );
}