//Tela de orçamento com exemplos
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { X, Plus } from "lucide-react";
import { useState } from "react";
import { usePessoas } from "@/hooks/usePessoas";

const tiposServico = ["Instalação", "Manutenção"];
const maquinas = ["D51", "Retroescavadeira"];
const pecas = ["Motor", "Parafusos X50"];

export default function OrcamentoPage() {
  const { data: pessoa, isLoading: pessoaLoading, addPessoa } = usePessoas();
  const [novoPessoa, setNovoPessoa] = useState("");
  const [pessoaSelecionado, setPessoaSelecionado] = useState<string | undefined>(undefined);
  const [maquinasSelecionadas, setMaquinasSelecionadas] = useState<string[]>(["D51", "Retroescavadeira"]);
  const [pecasSelecionadas, setPecasSelecionadas] = useState<string[]>(["Motor", "Parafusos X50"]);

  return (
    <div className="flex flex-col flex-1 px-1 py-4 md:px-8 md:py-10">
      <div className="max-w-2xl mx-auto w-full">
        <h2 className="text-center text-2xl md:text-3xl font-bold mb-2">NOVO ORÇAMENTO</h2>
        <div className="h-3 w-full bg-[#891B14] rounded" />
        {/* Form Container */}
        <form className="mt-6 bg-[#dddddd] rounded-2xl shadow-md pb-6 px-2 pt-5 space-y-2">
          <div className="flex flex-wrap md:space-x-8 gap-6 justify-between rounded-lg py-2 px-2 bg-[#bdbdbd]">
            {/* Left - Pessoa e Serviço */}
            <div className="flex-1 min-w-[220px] space-y-3">
              <div className="space-y-1">
                <div className="text-xs font-semibold">PESSOA</div>
                <Select onValueChange={setPessoaSelecionado}>
                  <SelectTrigger className="bg-white">
                    <SelectValue placeholder="Selecione um pessoa" />
                  </SelectTrigger>
                  <SelectContent>
                    {!pessoaLoading && pessoa && pessoa.length === 0 && (
                      <div className="px-2 py-1 text-muted-foreground text-xs">Nenhum pessoa</div>
                    )}
                    {!pessoaLoading && pessoa && pessoa.map((c: any) => (
                      <SelectItem key={c.id} value={c.nome}>{c.nome}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <div className="flex mt-1 gap-2">
                  <Input
                    placeholder="Nome do novo pessoa"
                    value={novoPessoa}
                    onChange={e => setNovoPessoa(e.target.value)}
                    className="bg-white"
                  />
                  <Button
                    type="button"
                    variant="secondary"
                    size="sm"
                    disabled={!novoPessoa.trim()}
                    onClick={async () => {
                      await addPessoa(novoPessoa.trim());
                      setNovoPessoa("");
                    }}
                  >
                    <Plus size={14} className="mr-1" />Adicionar
                  </Button>
                </div>
              </div>
              <div className="space-y-1">
                <div className="text-xs font-semibold">TIPOS DE SERVIÇO</div>
                <Select>
                  <SelectTrigger className="bg-white">
                    <SelectValue placeholder="Selecione um tipo de serviço" />
                  </SelectTrigger>
                  <SelectContent>
                    {tiposServico.map((t) => (
                      <SelectItem key={t} value={t}>{t}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="flex gap-2 mt-2">
                <div className="space-y-1 flex-1">
                  <div className="text-xs font-semibold">DATA INICIAL</div>
                  <Input className="bg-white" placeholder="__/__/__" />
                </div>
                <div className="space-y-1 flex-1">
                  <div className="text-xs font-semibold">VALIDADE</div>
                  <Input className="bg-white" placeholder="__/__/__" />
                </div>
                <div className="space-y-1 flex-1">
                  <div className="text-xs font-semibold">DATA FINAL</div>
                  <Input className="bg-white" placeholder="__/__/__" />
                </div>
              </div>
            </div>
            {/* Right - Maquinas & Peças */}
            <div className="flex-1 min-w-[220px] space-y-3">
              <div>
                <div className="flex items-center text-xs font-semibold gap-2 mb-1">
                  MAQUINAS MANIPULADAS
                  <Button variant="secondary" type="button" size="sm"><Plus className="mr-1" size={14}/>ADD</Button>
                </div>
                <Select>
                  <SelectTrigger className="bg-white">
                    <SelectValue placeholder="Selecione uma máquina" />
                  </SelectTrigger>
                  <SelectContent>
                    {maquinas.map((m) => (
                      <SelectItem key={m} value={m}>{m}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <div className="flex flex-wrap mt-1 gap-1">
                  {maquinasSelecionadas.map((m) => (
                    <span className="flex items-center bg-white px-2 py-0.5 border rounded-full mr-1 text-xs" key={m}>
                      {m}
                      <button type="button" className="ml-2 text-red-600 focus:outline-none"><X size={14}/></button>
                    </span>
                  ))}
                </div>
              </div>
              <div>
                <div className="flex items-center text-xs font-semibold gap-2 mb-1">
                  PEÇAS UTILIZADAS
                  <Button variant="secondary" type="button" size="sm"><Plus className="mr-1" size={14}/>ADD</Button>
                </div>
                <Select>
                  <SelectTrigger className="bg-white">
                    <SelectValue placeholder="Selecione uma peça" />
                  </SelectTrigger>
                  <SelectContent>
                    {pecas.map((p) => (
                      <SelectItem key={p} value={p}>{p}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <div className="flex flex-wrap mt-1 gap-1">
                  {pecasSelecionadas.map((p) => (
                    <span className="flex items-center bg-white px-2 py-0.5 border rounded-full mr-1 text-xs" key={p}>
                      {p}
                      <button type="button" className="ml-2 text-red-600 focus:outline-none"><X size={14}/></button>
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
          {/* Descrição */}
          <div className="mt-0">
            <div className="text-xs font-semibold mb-1">DESCRIÇÃO DO SERVIÇO</div>
            <Textarea className="bg-white" placeholder="Descreva aqui..." />
          </div>

          {/* Dados Execução */}
          <div className="bg-[#bdbdbd] rounded-md py-2 px-2 space-y-2 mt-2">
            <div className="text-center text-xs font-semibold mb-2">DADOS DE EXECUÇÃO</div>
            <div className="flex gap-4">
              <div className="flex-1">
                <div className="text-xs">HORAS EM SERVIÇO</div>
                <Input className="bg-white" />
              </div>
              <div className="flex-1 flex flex-col items-center">
                <span className="text-xs">QUILOMETRAGEM</span>
                <div className="flex gap-2 mt-1">
                  <Input className="bg-white w-16" placeholder="Ida" />
                  <Input className="bg-white w-16" placeholder="Volta" />
                </div>
              </div>
            </div>
          </div>
          {/* Dados Pagamento */}
          <div className="bg-[#bdbdbd] rounded-md py-2 px-2 mt-2">
            <div className="text-center text-xs font-semibold mb-2">DADOS DE PAGAMENTO</div>
            <div className="flex flex-row flex-wrap items-center gap-3 mb-2">
              <span className="text-xs">FORMA DE PAGAMENTO</span>
              <label className="flex items-center gap-1 text-xs"><input type="radio" name="pagto" />PIX</label>
              <label className="flex items-center gap-1 text-xs"><input type="radio" name="pagto" />BOLETO</label>
              <label className="flex items-center gap-1 text-xs"><input type="radio" name="pagto" />DINHEIRO</label>
            </div>
            <div className="flex flex-row flex-wrap items-center gap-3 mb-2">
              <span className="text-xs">CONDIÇÕES DE PAGAMENTO</span>
              <label className="flex items-center gap-1 text-xs"><input type="radio" name="cond" />À VISTA</label>
              <label className="flex items-center gap-1 text-xs"><input type="radio" name="cond" />50% NA ENTRADA</label>
              <label className="flex items-center gap-1 text-xs"><input type="radio" name="cond" />PARCELADO</label>
            </div>
            <div className="mt-2">
              <div className="text-xs mb-1">VALOR FINAL</div>
              <Input className="bg-white" />
            </div>
          </div>
          {/* Actions */}
          <div className="flex gap-4 mt-4 w-full justify-center">
            <Button type="submit" className="bg-[#d73f38] hover:bg-[#a12721] text-white font-semibold text-lg px-8">SALVAR</Button>
            <Button type="button" variant="secondary" className="bg-gray-500 hover:bg-gray-700 text-white font-semibold text-lg px-8">CANCELAR</Button>
          </div>
        </form>
      </div>
    </div>
  )
}
