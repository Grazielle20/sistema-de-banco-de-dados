import customtkinter as ctk
from tkinter import ttk
import mysql.connector 
from mysql.connector import Error
import os
from dotenv import load_dotenv
load_dotenv()

#Conexão ao banco de dados
def conectar_db():
    try:
        conn = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            database = os.getenv("DB_NAME")
        )
        if conn.is_connected():
            print("Conexão estabelecida com sucesso")
            return conn
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

#Fechar banco de dados
def fechar_db(conn):
    if conn.is_connected():
        conn.close()
        print("Conexão ao banco de dados fechada")
 
 #Inserir dados       
def inserir_dados():
    nome = entry_nome.get()
    descricao = entry_descricao.get()
    qtd = entry_qtd.get()
    preco = entry_preco.get()
    fornecedor = entry_fornecedor.get()
    
    if nome == "" or descricao == "" or qtd == "" or preco == "" or fornecedor == "":
        mensagem = "Preencha todos os campos corretamente!"
        mensagem_cadastrar.configure(text=mensagem)
    else:
        mensagem_cadastrar.configure(text="")    
        conn = conectar_db()
        cursor = conn.cursor()
    
        inserir = "INSERT INTO produtos (Nome, Descricao, Quantidade, Preco, Fornecedor) VALUES (%s, %s, %s, %s, %s)"
        dados = (nome, descricao, qtd, preco, fornecedor)
        cursor.execute(inserir, dados)
        conn.commit()
        cursor.close()
        fechar_db(conn)
    
        entry_nome.delete(0, "end")
        entry_descricao.delete(0, "end")
        entry_qtd.delete(0, "end")
        entry_preco.delete(0, "end")
        entry_fornecedor.delete(0, "end")

#Buscar dados
def buscar_dados():
    produto = entry_pesquisar.get()
    
    if entry_pesquisar.get() == "":
        mensagem = "Preencha o campo corretamente!"
        mensagem_pesquisar.configure(text=mensagem)
    else:    
        mensagem_pesquisar.configure(text="")
        conn = conectar_db()
        cursor = conn.cursor()
        
        pesquisar = "SELECT * FROM produtos Where Nome  LIKE %s"
        cursor.execute(pesquisar, ('%' + produto + '%',))
        for linha in tree.get_children():
            tree.delete(linha)
    
        for linha in  cursor.fetchall():
            tree.insert("", ctk.END, values=linha)
    
        cursor.close()
        fechar_db(conn)
        
        entry_pesquisar.delete(0, "end")

#Atualizar dados
def atualizar_dados():
    
    conn = conectar_db()
    cursor =conn.cursor()
    
    cursor.execute("SELECT * FROM produtos")
    linhas = cursor.fetchall()
    for linha in tree.get_children():
        tree.delete(linha)
        
    for linha in linhas:
        tree.insert("", ctk.END, values=linha)
    
    cursor.close()
    fechar_db(conn)
    
#Editar dados
def editar_dado():
    id = entry_id.get()
    coluna = opcao.get()
    dado = entry_dado.get()
    
    if id == "" or coluna == "" or dado == "":
        mensagem = "Preencha todos os campos corretamente!"
        mensagem_editar.configure(text=mensagem)
    else:
        mensagem_editar.configure(text="")
        conn = conectar_db()
        cursor = conn.cursor()
        
        if coluna == "Nome":
            editar = "UPDATE produtos SET Nome = %s WHERE id = %s"
            dados = (dado, id)
            cursor.execute(editar, dados)
            conn.commit()
            cursor.close()
            fechar_db(conn)
            
        if coluna == "Descrição":
            editar = "UPDATE produtos SET Descricao = %s WHERE id = %s"
            dados = (dado, id)
            cursor.execute(editar, dados)
            conn.commit()
            cursor.close()
            fechar_db(conn)
        
        if coluna == "Quantidade":
            editar = "UPDATE produtos SET Quantidade = %s WHERE id = %s"
            dados = (dado, id)
            cursor.execute(editar, dados)
            conn.commit()
            cursor.close()
            fechar_db(conn)
        
        if coluna == "Preço":
            editar = "UPDATE produtos SET Preco = %s WHERE id = %s"
            dados = (dado, id)
            cursor.execute(editar, dados)
            conn.commit()
            cursor.close()
            fechar_db(conn)
            
        if coluna == "Fornecedor":
            editar = "UPDATE produtos SET Fornecedor = %s WHERE id = %s"
            dados = (dado, id)
            cursor.execute(editar, dados)
            conn.commit()
            cursor.close()
            fechar_db(conn)
        
        else:
            print("Erro ao editar o dado!")
            cursor.close()
            fechar_db(conn)
        
        entry_id.delete(0, "end")
        entry_dado.delete(0, "end")
            
#Deletar dados
def deletar_dados():
    if entry_deletar.get() == "":
        mensagem = "Preencha o campo corretamente!"
        mensagem_deletar.configure(text=mensagem)
    else:    
        mensagem_deletar.configure(text="")
        conn = conectar_db()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM produtos Where ID = %s", (entry_deletar.get(),))
        conn.commit()
        cursor.close()
        fechar_db(conn)
        
        entry_deletar.delete(0, "end")
    
#Interface gráfica com customtkinter      
app = ctk.CTk()
app.title("Sistema de Banco de Dados")
app.after(5, lambda: app.state('zoomed'))

#Cadastrar Produtos
label_cadastrar = ctk.CTkLabel(app, text="Cadastrar Produto", font=('Arial', 18))
label_cadastrar.place(x=135, y=360)

label_nome = ctk.CTkLabel(app, text="Nome do Produto", font=('Arial', 12))
label_nome.place(x=50, y=410)

entry_nome = ctk.CTkEntry(app, placeholder_text="Digite o nome do produto", width=170)
entry_nome.place(x=180, y=410)

label_descricao = ctk.CTkLabel(app, text="Descrição", font=('Arial', 12))
label_descricao.place(x=50, y=450)
entry_descricao = ctk.CTkEntry(app, placeholder_text="Digite a descrição", width=170)
entry_descricao.place(x=180, y=450)

label_qtd = ctk.CTkLabel(app, text="Qtd.Estoque", font=('Arial', 12))
label_qtd.place(x=50, y=490)

entry_qtd = ctk.CTkEntry(app, placeholder_text="Digite a quantidade", width=170)
entry_qtd.place(x=180, y=490)

label_preco = ctk.CTkLabel(app, text="Preço Unitário", font=('Arial', 12))
label_preco.place(x=50, y=530)

entry_preco = ctk.CTkEntry(app, placeholder_text="Digite o preço", width=170)
entry_preco.place(x=180, y=530)

label_fornecedor = ctk.CTkLabel(app, text="Fornecedor", font=('Arial', 12))
label_fornecedor.place(x=50, y=570)

entry_fornecedor = ctk.CTkEntry(app, placeholder_text="Digite o fornecedor", width=170)
entry_fornecedor.place(x=180, y=570)

botao_cadastro = ctk.CTkButton(app, text="Cadastrar", width=230, command=inserir_dados)
botao_cadastro.place(x=80, y=630)

mensagem_cadastrar = ctk.CTkLabel(app, text="", text_color="red", font=('Arial', 12))
mensagem_cadastrar.place(x=80, y=660)

#Pesquisar Produtos
label_pesquisar = ctk.CTkLabel(app, text="Pesquisar Produto", font=('Arial', 18))
label_pesquisar.place(x=612, y=410)

entry_pesquisar = ctk.CTkEntry(app, placeholder_text="Digite o nome do produto", width=180)
entry_pesquisar.place(x=536, y=450)

botao_pesquisar = ctk.CTkButton(app, text="Pesquisar", width=130, command=buscar_dados)
botao_pesquisar.place(x=727, y=450)

mensagem_pesquisar = ctk.CTkLabel(app, text="", text_color="red", font=('Arial', 12))
mensagem_pesquisar.place(x=601, y=480)

#Editar Produtos
label_editar = ctk.CTkLabel(app, text="Editar Dado", font=('Arial', 18))
label_editar.place(x=1111, y=360)

label_id = ctk.CTkLabel(app, text="ID do Produto", font=('Arial', 12))
label_id.place(x=1027, y=400)

entry_id = ctk.CTkEntry(app, placeholder_text="Digite o ID do produto", width=180)
entry_id.place(x=1147, y=400)

label_opcoes = ctk.CTkLabel(app, text="Selecione a Coluna", font=('Arial', 12))
label_opcoes.place(x=1027, y=440)

opcao = ctk.CTkComboBox(app, width=180, values=["Nome", "Descrição", "Quantidade", "Preço", "Fornecedor"])
opcao.place(x=1147, y=440)

label_dado = ctk.CTkLabel(app, text="Novo Dado", font=('Arial', 12))
label_dado.place(x=1027, y=480)

entry_dado = ctk.CTkEntry(app, placeholder_text="Digite o novo dado", width=180)
entry_dado.place(x=1147, y=480)

botao_editar = ctk.CTkButton(app, text="Editar", width=230, command=editar_dado)
botao_editar.place(x=1068, y=540)

mensagem_editar = ctk.CTkLabel(app, text="", text_color="red", font=('Arial', 12))
mensagem_editar.place(x=1070, y=580)

#Deletar Produtos
label_deletar = ctk.CTkLabel(app, text="Deletar Produto", font=('Arial', 18))
label_deletar.place(x=623, y=530)

entry_deletar = ctk.CTkEntry(app, placeholder_text="Digite o ID do produto", width=180)
entry_deletar.place(x=536, y=570)

botao_deletar = ctk.CTkButton(app, text="Deletar", width=130, command=deletar_dados)
botao_deletar.place(x=727, y=570)

mensagem_deletar = ctk.CTkLabel(app, text="", text_color="red", font=('Arial', 12))
mensagem_deletar.place(x=601, y=600)

#Botão de atualizar dados
botao_atualizar = ctk.CTkButton(app, text="Atualizar", command=atualizar_dados)
botao_atualizar.place(x=612, y=287)

#Treeview
tree = ttk.Treeview(app, columns=('Id', 'Nome', 'Descrição', 'Qtd.Estoque', 'Preço', 'Fornecedor'), show='headings')
tree.heading('Id', text='ID')
tree.heading('Nome', text='Nome')
tree.heading('Descrição', text='Descrição')
tree.heading('Qtd.Estoque', text='Qtd.Estoque')
tree.heading('Preço', text='Preço')
tree.heading('Fornecedor', text='Fornecedor')
tree.place(x=80, y=20, height=240)

app.mainloop()