
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

const API_URL = "http://localhost:8000"; 

export function useCompras() {
  interface ErrorResponse {
    detail: string;
  }
  const queryClient = useQueryClient();
  const token = localStorage.getItem('accessToken');
  const query = useQuery({
    queryKey: ["compras"],
    queryFn: async () => {
      const res = await fetch(`${API_URL}/compras`,{
      headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}`},
      });
      const data = await res.json();
      return data;
    }
  });

  const addMutation = useMutation({
    mutationFn: async (data:any) => {
      const token = localStorage.getItem('accessToken');
      data.id_pessoa = parseInt(data.id_pessoa)

      console.log(data)
      const res = await fetch(`${API_URL}/compra`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}`},
        body: JSON.stringify(data)
        // body: JSON.stringify({ nome }),
      });
  
      if (!res.ok) throw new Error("Erro ao adicionar");
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["compras"] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      const res = await fetch(`${API_URL}/compra/${id}`, { method: "DELETE" });

      if (!res.ok) {
      // Lê o JSON da resposta de erro para obter o "detail"
        const errorData: ErrorResponse = await res.json();
        
        // Lança um novo erro com a mensagem vinda do backend
        throw new Error(errorData.detail || "Ocorreu um erro ao remover a compra.");
      }
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["compras"] });
    },
    onError: (error: Error) => {
    // 'error.message' agora contém a mensagem de "detail" do seu backend!
      alert(`Falha na remoção:, Não foi possível remover, a compra possuí vinculo com outro registro.`); // Exibe o erro para o usuário
  },
  });

  return {
    ...query,
    addCompra: addMutation.mutateAsync,
    removeCompra: deleteMutation.mutateAsync,
    isSaving: addMutation.isPending,
    isDeleting: deleteMutation.isPending,
  };
}


export async function fetchWithAuth(url: string, options: RequestInit = {}): Promise<Response> {
  // Pega o token do localStorage
  const token = localStorage.getItem('accessToken');

  // Prepara os cabeçalhos
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Se o token existir, adiciona ao cabeçalho de Autorização
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  // Monta a URL completa e faz a chamada fetch com as novas opções
  const fullUrl = `${API_URL}${url}`;
  
  const response = await fetch(fullUrl, {
    ...options,
    headers,
  });

  console.log(response)

  // Se a resposta for 401 (Não Autorizado), o token pode ser inválido/expirado
  if (response.status === 401) {
    localStorage.removeItem('accessToken');
    // Para simplificar, vamos lançar um erro que o useQuery pode capturar
    throw new Error('Sessão expirada. Por favor, faça o login novamente.');
  }

  return response;
}