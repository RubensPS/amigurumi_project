import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2

# Conectando ao banco de dados PostgreSQL
def conectar_bd():
    return psycopg2.connect(
        dbname="amigurumi", user="postgres", password="dbrps", host="localhost", port="5432"
    )

# Funções CRUD
def incluir_produto():
    nome = entry_nome.get()
    descricao = entry_descricao.get()
    preco = entry_preco.get()
    quantidade = entry_quantidade.get()
    
    if nome and preco and quantidade:
        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO produtos (nome, descricao, preco, quantidade) VALUES (%s, %s, %s, %s)",
                (nome, descricao, preco, quantidade),
            )
            conn.commit()
            conn.close()
            carregar_produtos()
            limpar_campos()
            messagebox.showinfo("Sucesso", "Produto incluído com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao incluir produto: {e}")
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")

def excluir_produto():
    produto_id = lista_produtos.selection()[0]
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = %s", (produto_id,))
        conn.commit()
        conn.close()
        carregar_produtos()
        messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao excluir produto: {e}")

def alterar_produto():
    produto_id = lista_produtos.selection()[0]
    nome = entry_nome.get()
    descricao = entry_descricao.get()
    preco = entry_preco.get()
    quantidade = entry_quantidade.get()
    
    if nome and preco and quantidade:
        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE produtos SET nome = %s, descricao = %s, preco = %s, quantidade = %s WHERE id = %s",
                (nome, descricao, preco, quantidade, produto_id),
            )
            conn.commit()
            conn.close()
            carregar_produtos()
            limpar_campos()
            messagebox.showinfo("Sucesso", "Produto alterado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao alterar produto: {e}")
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")

def buscar_produto():
    nome = entry_nome.get()
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, preco, quantidade FROM produtos WHERE nome LIKE %s", ('%' + nome + '%',))
        produtos = cursor.fetchall()
        conn.close()
        atualizar_lista(produtos)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar produto: {e}")

def carregar_produtos():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, preco, quantidade FROM produtos")
        produtos = cursor.fetchall()
        conn.close()
        atualizar_lista(produtos)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar produtos: {e}")

def atualizar_lista(produtos):
    lista_produtos.delete(*lista_produtos.get_children())
    for produto in produtos:
        lista_produtos.insert("", "end", iid=produto[0], values=produto)

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)

def on_select(event):
    # Pega o item selecionado
    selected_item = lista_produtos.selection()

    if selected_item:
        produto_id = selected_item[0]  # O primeiro item selecionado
        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            # Buscar o produto pelo ID
            cursor.execute("SELECT nome, descricao, preco, quantidade FROM produtos WHERE id = %s", (produto_id,))
            produto = cursor.fetchone()
            conn.close()
            
            if produto:
                # Preenche os campos com os dados do produto
                entry_nome.delete(0, tk.END)
                entry_nome.insert(0, produto[0])
                
                entry_descricao.delete(0, tk.END)
                entry_descricao.insert(0, produto[1])
                
                entry_preco.delete(0, tk.END)
                entry_preco.insert(0, produto[2])
                
                entry_quantidade.delete(0, tk.END)
                entry_quantidade.insert(0, produto[3])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar produto: {e}")

# Interface Tkinter
root = tk.Tk()
root.title("Cadastro de Produtos - Amigurumi")

# Labels e Entradas de Texto
tk.Label(root, text="Nome").grid(row=0, column=0, padx=0, pady=5, sticky='e')
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1, padx=0, pady=5, sticky='w')

tk.Label(root, text="Descrição").grid(row=1, column=0, padx=0, pady=5, sticky='e')
entry_descricao = tk.Entry(root)
entry_descricao.grid(row=1, column=1, padx=0, pady=5, sticky='w')

tk.Label(root, text="Preço").grid(row=2, column=0, padx=0, pady=5, sticky='e')
entry_preco = tk.Entry(root)
entry_preco.grid(row=2, column=1, padx=0, pady=5, sticky='w')

tk.Label(root, text="Quantidade").grid(row=3, column=0, padx=0, pady=5, sticky='e')
entry_quantidade = tk.Entry(root)
entry_quantidade.grid(row=3, column=1, padx=0, pady=5, sticky='w')

# Botões CRUD
btn_incluir = tk.Button(root, text="Incluir", command=incluir_produto)
btn_incluir.grid(row=0, column=2, padx=10, pady=5)

btn_excluir = tk.Button(root, text="Excluir", command=excluir_produto)
btn_excluir.grid(row=1, column=2, padx=10, pady=5)

btn_alterar = tk.Button(root, text="Alterar", command=alterar_produto)
btn_alterar.grid(row=2, column=2, padx=10, pady=5)

btn_buscar = tk.Button(root, text="Buscar", command=buscar_produto)
btn_buscar.grid(row=3, column=2, padx=10, pady=5)

btn_recarregar = tk.Button(root, text="Recarregar", command=carregar_produtos)
btn_recarregar.grid(row=4, column=2, padx=10, pady=5)

# Lista de Produtos
lista_produtos = ttk.Treeview(root, columns=("id", "nome", "preco", "quantidade"), show="headings")
lista_produtos.heading("id", text="ID")
lista_produtos.heading("nome", text="Nome")
lista_produtos.heading("preco", text="Preço")
lista_produtos.heading("quantidade", text="Quantidade")
lista_produtos.grid(row=5, column=0, columnspan=3, pady=10)

# Bind a função de seleção ao Treeview
lista_produtos.bind("<<TreeviewSelect>>", on_select)

# Inicializa a lista de produtos
carregar_produtos()

# Inicia a aplicação
root.mainloop()