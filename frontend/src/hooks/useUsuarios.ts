
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

const API_URL = "http://localhost:8000"; 

export function useUsuarios() {
  const queryClient = useQueryClient();

  const query = useQuery({
    queryKey: ["usuarios"],
    queryFn: async () => {
      const res = await fetch(`${API_URL}/usuarios`);
      const data = await res.json();
      return data;
    }
  });

  const addMutation = useMutation({
    mutationFn: async (data:any) => {
      console.log(JSON.stringify(data))
      const res = await fetch(`${API_URL}/usuario`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
        // body: JSON.stringify({ nome }),
      });
      if (!res.ok) throw new Error("Erro ao adicionar");
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["usuarios"] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      const res = await fetch(`${API_URL}/usuario/${id}`, { method: "DELETE" });
      if (!res.ok) throw new Error("Erro ao remover");
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["usuarios"] });
    },
  });

  return {
    ...query,
    addUsuario: addMutation.mutateAsync,
    removeUsuario: deleteMutation.mutateAsync,
    isSaving: addMutation.isPending,
    isDeleting: deleteMutation.isPending,
  };
}
