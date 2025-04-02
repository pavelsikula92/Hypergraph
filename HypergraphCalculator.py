import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from typing import List, Set, Tuple, TypeAlias

# --- Definice typů ---
Edge: TypeAlias = Tuple[str, ...]  # Hyperhrana je n-tice stringů
Edges: TypeAlias = List[Edge]     # Seznam hyperhran

# --- Třída Hypergraph --- (Zůstává stejná)
class Hypergraph:
    def __init__(self, edges: Edges = None):
        self.edges: Edges = []
        self.vertices: Set[str] = set()
        if edges:
            self.add_edges_from_list(edges)

    def add_edges_from_list(self, edges: Edges):
        for edge in edges:
            self.add_edge(edge)

    def add_edge(self, edge: Edge):
        if edge not in self.edges:
            self.edges.append(edge)
            self.vertices.update(edge)

    def vertex_degrees(self):
        degrees = {v: 0 for v in self.vertices}
        for edge in self.edges:
            for vertex in edge:
                degrees[vertex] += 1
        return degrees

    def edge_degrees(self):
        degrees = {}
        for i, edge in enumerate(self.edges):
            degrees[tuple(sorted(edge))] = len(edge)
        return degrees

    def connected_components(self):
        if not self.edges:
            return [set(self.vertices)] if self.vertices else []

        graph = nx.Graph()
        for v in self.vertices:
            graph.add_node(v)
        for edge in self.edges:
            edge_list = list(edge)
            for i in range(len(edge_list)):
                for j in range(i + 1, len(edge_list)):
                    graph.add_edge(edge_list[i], edge_list[j])

        components = list(nx.connected_components(graph))
        return components

    def visualize(self):
        """Vizualizuje hypergraf (hyperhrany jako kruhy)."""
        if not self.edges:
            messagebox.showinfo("Prázdný hypergraf", "Hypergraf je prázdný, není co vizualizovat.")
            return

        graph = nx.Graph()
        for v in self.vertices:
            graph.add_node(v)


        pos = nx.spring_layout(graph)


        viz_window = tk.Toplevel(root)
        viz_window.title("Vizualizace Hypergrafu")


        figure = plt.Figure(figsize=(8, 6))
        canvas = FigureCanvasTkAgg(figure, master=viz_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        ax = figure.add_subplot(111)


        nx.draw_networkx_nodes(graph, pos, node_color='skyblue', node_size=500, ax=ax)
        nx.draw_networkx_labels(graph, pos, ax=ax)


        for edge in self.edges:

            edge_positions = [pos[v] for v in edge]

            if not edge_positions:
                continue


            centroid = np.mean(edge_positions, axis=0)


            max_distance = 0
            for p in edge_positions:
                distance = np.linalg.norm(p - centroid)
                if distance > max_distance:
                    max_distance = distance


            circle = plt.Circle(centroid, max_distance, color='lightgray', alpha=0.5)
            ax.add_patch(circle)


        ax.autoscale_view()
        ax.set_aspect('equal')
        canvas.draw()

    def apply_rule(self, rule, iterations):
        """Aplikuje pravidlo na hypergraf po zadaný počet iterací."""
        current_edges = self.edges[:]
        for _ in range(iterations):
            current_edges = rule(current_edges, list(self.vertices))
            unique_edges = []
            for e in current_edges:
                if e not in unique_edges:
                    unique_edges.append(e)
            current_edges = unique_edges

        self.edges = current_edges
        self.vertices = set().union(*current_edges)

# --- Pravidlo (definice) ---
def pravidlo(hyperhrany: Edges, vrcholy: List[str]) -> Edges:
    """
    Pravidlo: Vytvoří kombinace, každý s každým.
    """
    nove_hyperhrany: Edges = []
    vrcholy_set = set(vrcholy)

    for v1 in vrcholy_set:
        for v2 in vrcholy_set:
            nove_hyperhrany.append(tuple(sorted((v1, v2))))

    unikatni_hrany = []
    for h in nove_hyperhrany:
        if h not in unikatni_hrany:
            unikatni_hrany.append(h)

    return unikatni_hrany



# --- GUI ---
def add_vertex():
    """Přidá vrchol do seznamu vrcholů."""
    vertex = vertex_entry.get().strip()
    if vertex:
        if vertex not in vertices_listbox.get(0, tk.END):  # Kontrola duplicit
            vertices_listbox.insert(tk.END, vertex)
        vertex_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Prázdný vrchol", "Zadejte název vrcholu.")

def remove_vertex():
    """Odstraní vybraný vrchol ze seznamu vrcholů."""
    try:
        selected_index = vertices_listbox.curselection()[0]
        vertices_listbox.delete(selected_index)
    except IndexError:
        messagebox.showwarning("Žádný vrchol nevybrán", "Vyberte vrchol k odstranění.")

def add_edge_gui():
    """Přidá hyperhranu na základě vybraných vrcholů."""
    selected_vertices = [vertices_listbox.get(i) for i in vertices_listbox.curselection()]
    if selected_vertices:
        new_edge = tuple(sorted(selected_vertices))
        if new_edge not in [tuple(sorted(eval(edge_str))) for edge_str in edges_listbox.get(0, tk.END)]:  # Kontrola duplicit, eval je bezpečné TADY
          edges_listbox.insert(tk.END, str(new_edge))
        else:
          messagebox.showwarning("Duplicitní hyperhrana", "Tato hyperhrana již existuje.")
    else:
        messagebox.showwarning("Žádné vrcholy nevybrány", "Vyberte vrcholy pro vytvoření hyperhrany.")

def remove_edge_gui():
    """Odstraní vybranou hyperhranu."""
    try:
        selected_index = edges_listbox.curselection()[0]
        edges_listbox.delete(selected_index)
    except IndexError:
        messagebox.showwarning("Žádná hyperhrana nevybrána", "Vyberte hyperhranu k odstranění.")


def generate_hypergraph_command():
    """Vytvoří hypergraf z dat z GUI."""
    global hypergraph
    try:
        edges = []
        for edge_str in edges_listbox.get(0, tk.END):
            edge = tuple(sorted(eval(edge_str))) # Znovu, eval je tady *bezpečné*
            edges.append(edge)
        hypergraph = Hypergraph(edges=edges)
        update_output()
    except Exception as e:
        messagebox.showerror("Chyba", f"Došlo k chybě: {e}")


def apply_rule_command():
    """Aplikuje pravidlo na hypergraf."""
    global hypergraph
    try:
        iterations = int(iterations_entry.get())
        if hypergraph:
            hypergraph.apply_rule(pravidlo, iterations)
            update_output()
        else:
            messagebox.showinfo("Hypergraf neexistuje", "Nejdříve vytvořte hypergraf.")
    except ValueError:
        messagebox.showerror("Chyba", "Neplatný vstup. Zadejte celé číslo pro počet iterací.")
    except Exception as e:
        messagebox.showerror("Chyba", f"Došlo k chybě: {e}")

def visualize_command():
    """Vizualizuje hypergraf."""
    if hypergraph:
        hypergraph.visualize()
    else:
        messagebox.showinfo("Hypergraf neexistuje", "Nejdříve vytvořte hypergraf.")


def clear_all():
    """Vyčistí všechna vstupní pole a výstup."""
    global hypergraph
    hypergraph = None
    vertex_entry.delete(0, tk.END)
    vertices_listbox.delete(0, tk.END)
    edges_listbox.delete(0, tk.END)
    iterations_entry.delete(0, tk.END)
    output_text.delete("1.0", tk.END)


def update_output():
    """Aktualizuje textové pole s výstupem."""
    if hypergraph:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Hyperhrany:\n")
        output_text.insert(tk.END, str(hypergraph.edges) + "\n\n")
        output_text.insert(tk.END, "Stupně vrcholů:\n")
        output_text.insert(tk.END, str(hypergraph.vertex_degrees()) + "\n\n")
        output_text.insert(tk.END, "Stupně hyperhran:\n")
        output_text.insert(tk.END, str(hypergraph.edge_degrees()) + "\n\n")
        output_text.insert(tk.END, "Komponenty souvislosti:\n")
        output_text.insert(tk.END, str(hypergraph.connected_components()) + "\n\n")

# --- Hlavní okno ---
root = tk.Tk()
root.title("Hypergrafová Kalkulačka")

# --- Proměnné ---
hypergraph = None

# --- Vstupní pole ---
input_frame = ttk.LabelFrame(root, text="Vstupní data")
input_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Zadávání vrcholů
vertex_label = ttk.Label(input_frame, text="Vrchol:")
vertex_label.grid(row=0, column=0, sticky=tk.W)
vertex_entry = ttk.Entry(input_frame)
vertex_entry.grid(row=0, column=1, sticky=tk.EW)
add_vertex_button = ttk.Button(input_frame, text="Přidat vrchol", command=add_vertex)
add_vertex_button.grid(row=0, column=2, sticky=tk.W)
remove_vertex_button = ttk.Button(input_frame, text="Odebrat vrchol", command=remove_vertex)
remove_vertex_button.grid(row=0, column=3, sticky=tk.E)


vertices_listbox = tk.Listbox(input_frame, selectmode="multiple")  # Pro výběr vrcholů
vertices_listbox.grid(row=1, column=0, columnspan=4, sticky=tk.EW)


# Hyperhrany
edges_label = ttk.Label(input_frame, text="Hyperhrany:")
edges_label.grid(row=2, column=0, sticky=tk.W)
add_edge_button = ttk.Button(input_frame, text="Přidat hyperhranu", command=add_edge_gui)
add_edge_button.grid(row=2, column=2, sticky=tk.W)
remove_edge_button = ttk.Button(input_frame, text="Odebrat hyperhranu", command=remove_edge_gui)
remove_edge_button.grid(row=2, column=3, sticky=tk.E)

edges_listbox = tk.Listbox(input_frame)  # Pro zobrazení hyperhran
edges_listbox.grid(row=3, column=0, columnspan=4, sticky=tk.EW)


# Počet iterací
iterations_label = ttk.Label(input_frame, text="Počet iterací:")
iterations_label.grid(row=4, column=0, sticky=tk.W)
iterations_entry = ttk.Entry(input_frame)
iterations_entry.grid(row=4, column=1, sticky=tk.EW)

# --- Tlačítka ---
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

generate_button = ttk.Button(button_frame, text="Generuj hypergraf", command=generate_hypergraph_command)
generate_button.pack(side=tk.LEFT, padx=5)

apply_rule_button = ttk.Button(button_frame, text="Aplikuj pravidlo", command=apply_rule_command)
apply_rule_button.pack(side=tk.LEFT, padx=5)

visualize_button = ttk.Button(button_frame, text="Vizualizuj", command=visualize_command)
visualize_button.pack(side=tk.LEFT, padx=5)

clear_button = ttk.Button(button_frame, text="Vyčistit", command=clear_all)
clear_button.pack(side=tk.LEFT, padx=5)

# --- Výstupní textové pole ---
output_frame = ttk.LabelFrame(root, text="Výstup")
output_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

output_text = tk.Text(output_frame, height=10, width=40)
output_text.pack()

# Konfigurace roztahování
input_frame.columnconfigure(1, weight=1) # Vstupní pole se roztáhne
root.columnconfigure(0, weight=1) # Aby se roztahoval input_frame
root.rowconfigure(1, weight=1)  # Aby se roztahoval output_frame



if __name__ == "__main__":
    root.mainloop()