// Em uma página como `src/pages/Index.tsx`

import UserTypeDashboard from '@/components/UserTypeDashboard';
import TotalDiaDashboard from '@/components/TotalPorDiaChart';

export default function Index() {
  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-6">Dashboard Principal</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Outros componentes do dashboard podem ir aqui */}
        
        {/* Componente do gráfico de usuários */}
        <UserTypeDashboard />

        {/* Exemplo de outro card no dashboard */}
        <div className="p-4 bg-white rounded-lg shadow-md">
          <TotalDiaDashboard />
        </div>
      </div>
    </div>
  );
}