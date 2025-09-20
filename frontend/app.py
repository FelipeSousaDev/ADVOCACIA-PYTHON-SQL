import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import re
import sys
import os

    # Adiciona o diretório raiz do projeto ao PATH
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

    # Solução para o erro do tkinter em ambientes virtuais
os.environ['TCL_LIBRARY'] = r"C:\Users\FELIPE\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\FELIPE\AppData\Local\Programs\Python\Python313\tcl\tk8.6"

    # Importa as classes e funções necessárias do backend
from backend.clientes_crud import Cliente, create_cliente, get_all_clientes, delete_cliente, update_cliente


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestão de Clientes - ADVOCACIA")
        self.geometry("800x600")
        self.resizable(True, True)

        style = ttk.Style(self)
        style.theme_use('clam')

        self.create_widgets()

    def create_widgets(self):
        # Frame principal para centralizar o conteúdo
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Titulo da página
        titulo = ttk.Label(main_frame, text="Menu Principal", font=("Helvetica", 16, "bold"))
        titulo.pack(pady=10)

        # Frame para os botões do menu
        menu_frame = ttk.Frame(main_frame)
        menu_frame.pack(pady=20)

        # Botão para abrir a tela de cadastro
        btn_cadastro = ttk.Button(menu_frame, text="Cadastrar Novo Cliente", command=self.abrir_tela_cadastro)
        btn_cadastro.pack(fill="x", pady=5)

        # Novo botão para abrir a tela de visualização
        btn_visualizar = ttk.Button(menu_frame, text="Visualizar Clientes", command=self.abrir_tela_visualizacao)
        btn_visualizar.pack(fill="x", pady=5)

    def abrir_tela_cadastro(self):
        # Cria uma nova janela toplevel
        janela_cadastro = Toplevel(self)
        janela_cadastro.title("Cadastro de Clientes")
        janela_cadastro.geometry("400x350")
        janela_cadastro.resizable(False, False)

        # Código do formulário
        form_frame = ttk.Frame(janela_cadastro, padding="20")
        form_frame.pack(fill="both", expand=True)

        titulo = ttk.Label(form_frame, text="Cadastro de Novo Cliente", font=("Helvetica", 14, "bold"))
        titulo.pack(pady=10)

        # Frame para os campos de entrada, usando grid para melhor controle de layout
        campos_frame = ttk.Frame(form_frame)
        campos_frame.pack()

        # Dicionário para armazenar as variáveis de controle dos campos de entrada
        self.campos = {}
        campos_info = {
            "Nome": "NOME",
            "CPF": "CPF",
            "Telefone": "TELEFONE",
            "Email": "EMAIL"
        }

        row_index = 0
        for label_text, campo_key in campos_info.items():
            label = ttk.Label(campos_frame, text=f"{label_text}:")
            label.grid(row=row_index, column=0, sticky="w", pady=(5, 0))
            entry_var = tk.StringVar()
            entry = ttk.Entry(campos_frame, textvariable=entry_var, width=40)
            entry.grid(row=row_index, column=1, sticky="e", pady=(0, 10))
            self.campos[campo_key] = entry_var
            row_index += 1

        # Botão para Salvar
        btn_salvar = ttk.Button(form_frame, text="Cadastrar novo cliente", command=self.salvar_cliente)
        btn_salvar.pack(fill="x", pady=20)

    def salvar_cliente(self):
        nome = self.campos["NOME"].get()
        cpf = self.campos["CPF"].get()
        telefone = self.campos["TELEFONE"].get()
        email = self.campos["EMAIL"].get()

        if not nome or not cpf:
            messagebox.showerror("Erro de validação", "Nome e CPF são campos obrigatórios")
            return

        #Valida CPF
        cpf_limpo = re.sub(r'\D', '', cpf)

        if len(cpf_limpo) != 11:
            messagebox.showerror("Erro de validação:", "CPF Inválido. Deve conter exatamente 11 digitos numéricos")
            return

        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,3}$'
        if not(re.match(email_regex, email)):
            messagebox.showerror("Erro de validação", "Formato de email invalido")
            return

        novo_cliente = Cliente(nome, telefone, email, cpf_limpo)

        if create_cliente(novo_cliente):
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            self.limpar_campos()
        else:
            messagebox.showerror("Erro", "Ocorreu um erro ao cadastrar o cliente")

    def limpar_campos(self):
        for var in self.campos.values():
            var.set("")

    def abrir_tela_visualizacao(self):
        janela_visualizacao = Toplevel(self)
        janela_visualizacao.title("Lista de clientes")
        janela_visualizacao.geometry("800x600")

        titulo = ttk.Label(janela_visualizacao, text="Lista de Clientes", font=("Helvetica", 16, "bold"))
        titulo.pack(pady=10)

        tabela_frame = ttk.Frame(janela_visualizacao)
        tabela_frame.pack(fill="both", expand=True, padx=10, pady=10)

        colunas = ('id', 'nome', 'cpf', 'telefone', 'email')
        tabela = ttk.Treeview(tabela_frame, columns=colunas, show='headings')

        tabela.heading('id', text='ID')
        tabela.heading('nome', text='Nome')
        tabela.heading('cpf', text='CPF')
        tabela.heading('telefone', text='Telefone')
        tabela.heading('email', text='Email')

        tabela.column('id', width=50, anchor='center')
        tabela.column('nome', width=200)
        tabela.column('cpf', width=120)
        tabela.column('telefone', width=100)
        tabela.column('email', width=200)

        scrollbar = ttk.Scrollbar(tabela_frame, orient=tk.VERTICAL, command=tabela.yview)
        tabela.configure(yscrollcommand=scrollbar.set)
        tabela.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def recarregar_tabela():
            for i in tabela.get_children():
                tabela.delete(i)
            clientes = get_all_clientes()
            for cliente in clientes:
                tabela.insert('', 'end',
                              values=(cliente.id, cliente.nome, cliente.cpf, cliente.telefone, cliente.email))

        recarregar_tabela()

        def on_delete():
            item_id = tabela.focus()
            if not item_id:
                messagebox.showerror("Erro", "Selecione um cliente para excluir.")
                return

            cliente_id = tabela.item(item_id, 'values')[0]
            if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o cliente ID {cliente_id}?"):
                if delete_cliente(cliente_id):
                    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
                    recarregar_tabela()
                else:
                    messagebox.showerror("Erro", "Ocorreu um erro ao excluir o cliente.")

        def on_edit(event):
            item_id = tabela.focus()
            if not item_id:
                return

            coluna_id = tabela.identify_column(event.x)
            coluna_clicada = tabela.heading(coluna_id)['text']

            if coluna_clicada in ['ID']:
                return

            x, y, width, height = tabela.bbox(item_id, coluna_id)

            valor_atual = tabela.item(item_id, 'values')[int(coluna_id.replace('#', '')) - 1]
            editor = ttk.Entry(tabela_frame)
            editor.insert(0, valor_atual)
            editor.place(x=x, y=y, width=width, height=height)
            editor.focus()

            def on_save(event_save):
                novo_valor = editor.get()
                if novo_valor != valor_atual:
                    valores_atuais = list(tabela.item(item_id, 'values'))
                    colunas = ['ID', 'Nome', 'CPF', 'Telefone', 'Email']

                    valores_atuais[int(coluna_id.replace('#', '')) - 1] = novo_valor

                    cliente_id = valores_atuais[0]
                    novo_cliente = Cliente(
                        nome=valores_atuais[1],
                        cpf=valores_atuais[2],
                        telefone=valores_atuais[3],
                        email=valores_atuais[4],
                        id=cliente_id
                    )

                    if update_cliente(novo_cliente):
                        tabela.item(item_id, values=valores_atuais)
                        messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
                        recarregar_tabela()
                    else:
                        messagebox.showerror("Erro", "Ocorreu um erro ao atualizar o cliente.")

                editor.destroy()

            editor.bind('<Return>', on_save)
            editor.bind('<FocusOut>', on_save)

        tabela.bind('<Double-1>', on_edit)

        botoes_frame = ttk.Frame(janela_visualizacao)
        botoes_frame.pack(pady=10)

        btn_excluir = ttk.Button(botoes_frame, text="Excluir Cliente", command=on_delete)
        btn_excluir.pack(side=tk.LEFT, padx=5)



def run_app():
    app = App()
    app.mainloop()

