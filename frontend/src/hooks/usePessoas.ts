
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

const API_URL = "http://localhost:8000"; 

const tipoPessoaFisica=0;

export function usePessoas() {
  const queryClient = useQueryClient();
  const token = localStorage.getItem('accessToken');
  const query = useQuery({
    queryKey: ["pessoas", tipoPessoaFisica],
    queryFn: async () => {
      const res = await fetch(`${API_URL}/pessoas/${tipoPessoaFisica}`,{
      headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}`},
      });
      const data = await res.json();
      return data;
    }
  });

  const addMutation = useMutation({
    mutationFn: async (data:any) => {
      const token = localStorage.getItem('accessToken');

      const res = await fetch(`${API_URL}/pessoa`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}`},
        body: JSON.stringify(data)
        // body: JSON.stringify({ nome }),
      });
  
      if (!res.ok) throw new Error("Erro ao adicionar");
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["pessoas"] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      const res = await fetch(`${API_URL}/pessoa/${id}`, { method: "DELETE" });
      if (!res.ok) throw new Error("Erro ao remover");
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["pessoas"] });
    },
  });

  return {
    ...query,
    addPessoa: addMutation.mutateAsync,
    removePessoa: deleteMutation.mutateAsync,
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