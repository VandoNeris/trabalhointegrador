import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";


const API_URL = "http://localhost:8000";

export async function fetchWithAuth(url: string, options: RequestInit = {}): Promise<Response> {
  const token = localStorage.getItem('accessToken');
  const headers = { 'Content-Type': 'application/json', ...options.headers };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(url, { ...options, headers });

  if (response.status === 401) {
    localStorage.removeItem('accessToken');
    throw new Error('Sessão expirada. Por favor, faça o login novamente.');
  }

  return response;
}


export function useCompras() {
  interface ErrorResponse { detail: string; }
  const queryClient = useQueryClient();

  // GET (Listar)
  const query = useQuery({
    queryKey: ["compras"],
    queryFn: async () => {
      const res = await fetchWithAuth(`${API_URL}/compras`);
      return res.json();
    }
  });


  const addMutation = useMutation({
    mutationFn: async (data: any) => {
      data.id_pessoa = parseInt(data.id_pessoa);
      const res = await fetchWithAuth(`${API_URL}/compra`, {
        method: "POST",
        body: JSON.stringify(data)
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
      const res = await fetchWithAuth(`${API_URL}/compra/${id}`, { method: "DELETE" });

      if (!res.ok) {
        const errorData: ErrorResponse = await res.json();
        throw new Error(errorData.detail || "Ocorreu um erro ao remover a compra.");
      }

      if (res.status === 204) return;
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["compras"] });
    },
    onError: (error: Error) => {
      alert(`Falha na remoção: ${error.message}`);
    },
  });

  interface UpdateCompraData {
  id: number;
  data: any;
}

  const updateMutation = useMutation({
    mutationFn: async ({ id, data }: UpdateCompraData) => {
      const res = await fetchWithAuth(`${API_URL}/compra/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      });

      if (!res.ok) {

        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || "Erro ao atualizar a compra.");
      }
      return res.json();
    },
    onSuccess: () => {

      queryClient.invalidateQueries({ queryKey: ["compras"] });
    },
    onError: (error: Error) => {
        alert(`Falha na atualização: ${error.message}`);
    }
  });

  return {
    ...query,
    addCompra: addMutation.mutateAsync,
     updateCompra: updateMutation.mutateAsync,
    removeCompra: deleteMutation.mutateAsync,
    isSaving: addMutation.isPending,
    isDeleting: deleteMutation.isPending,
    isUpdating: updateMutation.isPending,
  };
}