//Tela de estoque com exemplos
import { Plus, Eye, Save } from "lucide-react";

const produtos = [
  { id: 1, nome: "PARAFUSO", marca: "ABC", categoria: "FIXADORES", maquina: "D51", quantidade: 150 },
  { id: 2, nome: "Komatsu SAA6D107E-1", marca: "Komatsu", categoria: "MOTOR", maquina: "D51", quantidade: 2 },
  { id: 3, nome: "Dentes Caçamba", marca: "Randon", categoria: "Dentes", maquina: "Retroescavadeira", quantidade: 6 },
];

export default function EstoquePage() {
  return (
    <div className="flex flex-col flex-1 px-2 py-6 md:px-8 md:py-8">
      <div className="max-w-4xl mx-auto w-full">
        <h2 className="text-2xl md:text-3xl font-bold mb-3">ESTOQUE</h2>
        <div className="h-3 w-full bg-[#891B14] rounded mb-3" />

        {/* Filtros */}
        <div className="flex flex-col md:flex-row gap-3 mb-4">
          <input placeholder="Pesquisar por nome ou id" className="bg-[#dddddd] rounded px-3 py-2 w-full md:w-[220px]"/>
          <input placeholder="Marca" className="bg-[#dddddd] rounded px-3 py-2 w-full md:w-[180px]"/>
          <input placeholder="Categoria" className="bg-[#dddddd] rounded px-3 py-2 w-full md:w-[180px]"/>
          <input placeholder="Máquina" className="bg-[#dddddd] rounded px-3 py-2 w-full md:w-[180px]"/>
          <button className="bg-[#891B14] hover:bg-[#ad3c36] text-white font-semibold px-4 py-2 rounded flex items-center"><Plus className="mr-1" size={18}/> CADASTRAR PRODUTO</button>
        </div>
        {/* Tabela */}
        <div className="rounded-xl overflow-hidden bg-[#dddddd]">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-[#bdbdbd]">
                <th className="py-2 px-3">ID</th>
                <th className="py-2 px-3">NOME</th>
                <th className="py-2 px-3">MARCA</th>
                <th className="py-2 px-3">CATEGORIA</th>
                <th className="py-2 px-3">MÁQUINA</th>
                <th className="py-2 px-3">QUANTIDADE</th>
                <th className="py-2 px-3">AÇÕES</th>
              </tr>
            </thead>
            <tbody>
              {produtos.map((prod) => (
                <tr key={prod.id} className="border-b last:border-b-0 text-center">
                  <td className="py-2">{prod.id}</td>
                  <td className="py-2">{prod.nome}</td>
                  <td className="py-2">{prod.marca}</td>
                  <td className="py-2">{prod.categoria}</td>
                  <td className="py-2">{prod.maquina}</td>
                  <td className="py-2">{prod.quantidade}</td>
                  <td className="py-2 flex gap-2 justify-center items-center">
                    <button title="Editar" className="hover:text-[#891B14] p-1"><Save size={18}/></button>
                    <button title="Ver" className="hover:text-[#891B14] p-1"><Eye size={18}/></button>
                  </td>
                </tr>
              ))}

              {Array.from({ length: 3 }).map((_, i) => (
                <tr key={`empty-${i}`}>
                  <td colSpan={7} className="py-4" />
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
