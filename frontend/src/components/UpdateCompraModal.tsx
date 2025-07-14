import React, { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Button } from '@/components/ui/button';
import { format, parseISO } from 'date-fns'; // 

interface Pessoa { id_pessoa: number; nome: string; }
interface CompraData {
  id_compra: number;
  loc_entrega: string;
  valor: number;
  dt_emissao: string;
  dt_vencimento: string;
  dt_entrega?: string | null;
  dt_pagamento?: string | null;
  id_pessoa: number;
}
interface UpdateModalProps {
  compra: CompraData;
  pessoas: Pessoa[];
  onClose: () => void;
  onSave: (data: Omit<CompraData, 'id_compra'>) => void;
  isUpdating: boolean;
}

const formatDateForInput = (dateString: string | null | undefined) => {
  if (!dateString) return '';
  try {
    const date = parseISO(dateString);
    return format(date, 'yyyy-MM-dd');
  } catch (error) {
    console.error("Data inválida recebida:", dateString);
    return ''; 
  }
};


export const UpdateCompraModal: React.FC<UpdateModalProps> = ({ compra, pessoas, onClose, onSave, isUpdating }) => {
  const [formData, setFormData] = useState({
    ...compra,
    dt_emissao: formatDateForInput(compra.dt_emissao),
    dt_vencimento: formatDateForInput(compra.dt_vencimento),
    dt_entrega: formatDateForInput(compra.dt_entrega),
    dt_pagamento: formatDateForInput(compra.dt_pagamento),
  });

  useEffect(() => {
    setFormData({
      ...compra,
      dt_emissao: formatDateForInput(compra.dt_emissao),
      dt_vencimento: formatDateForInput(compra.dt_vencimento),
      dt_entrega: formatDateForInput(compra.dt_entrega),
      dt_pagamento: formatDateForInput(compra.dt_pagamento),
    });
  }, [compra]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({ ...prev, [name]: type === 'number' ? parseFloat(value) || 0 : value, }));
  };

  const handleSelectChange = (id_pessoa: string) => {
    setFormData(prev => ({ ...prev, id_pessoa: parseInt(id_pessoa, 10) }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const { id_compra, ...dataToSave } = formData;
    const finalData = {
      ...dataToSave,
      dt_entrega: dataToSave.dt_entrega || null,
      dt_pagamento: dataToSave.dt_pagamento || null
    };
    onSave(finalData);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
        <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-lg">
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold">Editar Compra #{compra.id_compra}</h2>
                <button onClick={onClose} className="hover:text-red-500"><X size={24} /></button>
            </div>
            <form onSubmit={handleSubmit} className="space-y-4 max-h-[70vh] overflow-y-auto pr-2">
                <div>
                    <label className="block text-sm font-medium text-gray-700">Comprador</label>
                    <Select value={String(formData.id_pessoa)} onValueChange={handleSelectChange}>
                        <SelectTrigger><SelectValue /></SelectTrigger>
                        <SelectContent>
                            {pessoas.map(p => (
                                <SelectItem key={p.id_pessoa} value={String(p.id_pessoa)}>{p.nome}</SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                </div>
                <div>
                    <label htmlFor="loc_entrega" className="block text-sm font-medium text-gray-700">Local de Entrega</label>
                    <Input type="text" id="loc_entrega" name="loc_entrega" value={formData.loc_entrega} onChange={handleChange} />
                </div>
                <div>
                    <label htmlFor="valor" className="block text-sm font-medium text-gray-700">Valor</label>
                    <Input type="number" id="valor" name="valor" value={formData.valor} onChange={handleChange} />
                </div>
                <div className='grid grid-cols-2 gap-4'>
                    <div>
                        <label htmlFor="dt_emissao" className="block text-sm font-medium text-gray-700">Data de Emissão</label>
                        <Input type="date" id="dt_emissao" name="dt_emissao" value={formData.dt_emissao} onChange={handleChange} />
                    </div>
                    <div>
                        <label htmlFor="dt_vencimento" className="block text-sm font-medium text-gray-700">Data de Vencimento</label>
                        <Input type="date" id="dt_vencimento" name="dt_vencimento" value={formData.dt_vencimento} onChange={handleChange} />
                    </div>
                    <div>
                        <label htmlFor="dt_entrega" className="block text-sm font-medium text-gray-700">Data de Entrega (Opcional)</label>
                        <Input type="date" id="dt_entrega" name="dt_entrega" value={formData.dt_entrega || ''} onChange={handleChange} />
                    </div>
                    <div>
                        <label htmlFor="dt_pagamento" className="block text-sm font-medium text-gray-700">Data de Pagamento (Opcional)</label>
                        <Input type="date" id="dt_pagamento" name="dt_pagamento" value={formData.dt_pagamento || ''} onChange={handleChange} />
                    </div>
                </div>
                <div className="flex justify-end gap-4 pt-4">
                    <Button type="button" variant="secondary" onClick={onClose}>Cancelar</Button>
                    <Button type="submit" disabled={isUpdating}>
                        {isUpdating ? 'Salvando...' : 'Salvar Alterações'}
                    </Button>
                </div>
            </form>
        </div>
    </div>
  );
};
