
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

const API_URL = "http://localhost:8000"; 

const tipoPessoaJuridica=1;

export function useEmpresas() {
  const queryClient = useQueryClient();

  const query = useQuery({
    queryKey: ["pessoas"],
    queryFn: async () => {
      const res = await fetch(`${API_URL}/pessoas/${tipoPessoaJuridica}`);
      const data = await res.json();
      return data;
    }
  });

  const addMutation = useMutation({
    mutationFn: async (data:any) => {
      console.log(JSON.stringify(data))
      const res = await fetch(`${API_URL}/pessoa`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
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
    addEmpresa: addMutation.mutateAsync,
    removeEmpresa: deleteMutation.mutateAsync,
    isSaving: addMutation.isPending,
    isDeleting: deleteMutation.isPending,
  };
}
