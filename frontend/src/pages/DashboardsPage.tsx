

import UserTypeDashboard from '@/components/UserTypeDashboard';
import TotalPorDiaChart from '@/components/TotalPorDiaChart'; 
import { useCompras } from '@/hooks/useCompras'; 
import { useMemo } from 'react';


interface Compra {
  dt_emissao: string; 
  valor: number;

}

export default function DashboardsPage() {
  const { data: compras, isLoading, isError, error } = useCompras();

  const dadosDoGrafico = useMemo(() => {
    if (!compras) return [];

    const totaisPorDia = (compras as Compra[]).reduce((acc, compra) => {
      const dia = compra.dt_emissao.split('T')[0]; 
      if (!acc[dia]) {
        acc[dia] = 0;
      }
      acc[dia] += compra.valor;
      return acc;
    }, {} as Record<string, number>);

    // Converte o objeto em um array no formato { data, total }
    return Object.entries(totaisPorDia)
      .map(([data, total]) => ({ data, total }))
      .sort((a, b) => new Date(a.data).getTime() - new Date(b.data).getTime()); // Ordena por data

  }, [compras]); // useMemo otimiza para não re-calcular a cada renderização

  if (isError) {
    return <div>Erro ao carregar dados: {error instanceof Error ? error.message : 'Erro desconhecido'}</div>;
  }
  
  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-6">Dashboard Principal</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <UserTypeDashboard />

        {/* Passando os dados processados e o estado de carregamento para o gráfico */}
        <TotalPorDiaChart 
          dados={dadosDoGrafico} 
          isLoading={isLoading}
          titulo="Total de Compras por Dia"
        />
      </div>
    </div>
  );
}