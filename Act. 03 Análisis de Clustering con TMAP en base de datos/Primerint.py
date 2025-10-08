import umap
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import matplotlib.patches as mpatches


# Cargar datos sin pandas
def load_fashion_mnist(file_path):
    print(f"Cargando datos desde: {file_path}")
    data = np.loadtxt(file_path, delimiter=',', skiprows=1)
    labels = data[:, 0].astype(int)
    images = data[:, 1:].reshape(-1, 28, 28)
    return images, labels


# Cargar el dataset
try:
    images, labels = load_fashion_mnist("C:/Users/Jose-/OneDrive/Desktop/Analisis de Algoritmo/fashion-mnist_test.csv")
    print(f"✅ Datos cargados: {images.shape[0]} imágenes, {images.shape[1]}x{images.shape[2]} píxeles")
except:
    print("❌ No se pudo cargar el archivo, usando datos de ejemplo...")
    # Datos de ejemplo si no carga el archivo
    from sklearn.datasets import fetch_openml

    fashion_mnist = fetch_openml('Fashion-MNIST', version=1, as_frame=False, parser='auto')
    images = fashion_mnist.data.reshape(-1, 28, 28)
    labels = fashion_mnist.target.astype(int)

# Nombres de las clases
class_names = {
    0: 'T-shirt/top',
    1: 'Trouser',
    2: 'Pullover',
    3: 'Dress',
    4: 'Coat',
    5: 'Sandal',
    6: 'Shirt',
    7: 'Sneaker',
    8: 'Bag',
    9: 'Ankle boot'
}

# Preprocesamiento: aplanar imágenes y normalizar
print("Preprocesando datos...")
X_flat = images.reshape(images.shape[0], -1)
scaler = StandardScaler()
X_normalized = scaler.fit_transform(X_flat)

# Tomar muestra para hacerlo más rápido (opcional)
sample_size = min(5000, len(X_normalized))
np.random.seed(42)
sample_indices = np.random.choice(len(X_normalized), sample_size, replace=False)
X_sample = X_normalized[sample_indices]
labels_sample = labels[sample_indices]

print(f"Tamaño de la muestra para UMAP: {X_sample.shape}")

# === APLICACIÓN DE UMAP SOBRE EL CONJUNTO COMPLETO ===
print("Aplicando UMAP sobre el conjunto completo...")

# Configurar y aplicar UMAP
reducer = umap.UMAP(n_components=2, random_state=42, n_neighbors=15, min_dist=0.1)
embedding = reducer.fit_transform(X_sample)

print("✅ UMAP completado")


# Visualización de UMAP para el conjunto completo
def plot_umap_full(embedding, labels, class_names, title="UMAP - Fashion MNIST Completo"):
    plt.figure(figsize=(15, 12))

    scatter = plt.scatter(embedding[:, 0], embedding[:, 1],
                          c=labels, cmap='tab10', s=5, alpha=0.7)

    # Crear leyenda
    legend_elements = []
    for class_id, class_name in class_names.items():
        if class_id in labels:
            legend_elements.append(mpatches.Patch(
                color=plt.cm.tab10(class_id / 10),
                label=f'{class_id}: {class_name}'
            ))

    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
    plt.title(title, fontsize=16)
    plt.xlabel('UMAP Dimension 1')
    plt.ylabel('UMAP Dimension 2')
    plt.tight_layout()
    plt.show()


plot_umap_full(embedding, labels_sample, class_names)

# === SELECCIÓN DE UN CLUSTER ESPECÍFICO ===
print("\nSeleccionando cluster de calzado...")
shoe_classes = [5, 7, 9]  # Sandal, Sneaker, Ankle boot
shoe_mask = np.isin(labels_sample, shoe_classes)
X_shoes = X_sample[shoe_mask]
labels_shoes = labels_sample[shoe_mask]
shoe_indices = sample_indices[shoe_mask]

print(f"Tamaño del cluster de calzado: {X_shoes.shape[0]} imágenes")

# === APLICAR UMAP SOBRE EL SUBSET DE CALZADO ===
print("Aplicando UMAP al cluster de calzado...")
reducer_shoes = umap.UMAP(n_components=2, random_state=42, n_neighbors=10, min_dist=0.1)
embedding_shoes = reducer_shoes.fit_transform(X_shoes)


# Visualización del cluster de calzado
def plot_shoe_cluster(embedding, labels, class_names, title="UMAP - Cluster de Calzado"):
    plt.figure(figsize=(12, 10))

    # Mapear colores específicos para calzado
    color_map = {5: 0, 7: 1, 9: 2}
    colors = [color_map[label] for label in labels]

    scatter = plt.scatter(embedding[:, 0], embedding[:, 1],
                          c=colors, cmap='Set2', s=20, alpha=0.8)

    # Leyenda personalizada para calzado
    shoe_legend_elements = [
        mpatches.Patch(color=plt.cm.Set2(0), label='Sandal'),
        mpatches.Patch(color=plt.cm.Set2(1), label='Sneaker'),
        mpatches.Patch(color=plt.cm.Set2(2), label='Ankle boot')
    ]

    plt.legend(handles=shoe_legend_elements, loc='upper right')
    plt.title(title, fontsize=16)
    plt.xlabel('UMAP Dimension 1')
    plt.ylabel('UMAP Dimension 2')
    plt.tight_layout()
    plt.show()


plot_shoe_cluster(embedding_shoes, labels_shoes, class_names)

# === IDENTIFICACIÓN DE SUBCLUSTERS ===
print("Identificando subclusters...")
dbscan = DBSCAN(eps=0.5, min_samples=5)
subcluster_labels = dbscan.fit_predict(embedding_shoes)

n_subclusters = len(set(subcluster_labels)) - (1 if -1 in subcluster_labels else 0)
print(f"Número de subclusters identificados: {n_subclusters}")
print(f"Puntos considerados como ruido: {np.sum(subcluster_labels == -1)}")


# === VISUALIZACIÓN DE SUBCLUSTERS ===
def plot_subclusters(embedding, subcluster_labels, original_labels, class_names, title="Subclusters en Calzado"):
    plt.figure(figsize=(14, 10))

    scatter = plt.scatter(embedding[:, 0], embedding[:, 1],
                          c=subcluster_labels, cmap='tab20', s=30, alpha=0.8)

    # Añadir etiquetas de clase original para algunos puntos
    for i, (xi, yi, orig_label) in enumerate(zip(embedding[:, 0], embedding[:, 1], original_labels)):
        if i % 15 == 0:  # Mostrar solo algunas etiquetas para evitar saturación
            plt.annotate(class_names[orig_label], (xi, yi), fontsize=8, alpha=0.7)

    plt.colorbar(scatter, label='Subcluster')
    plt.title(title, fontsize=16)
    plt.xlabel('UMAP Dimension 1')
    plt.ylabel('UMAP Dimension 2')
    plt.tight_layout()
    plt.show()


plot_subclusters(embedding_shoes, subcluster_labels, labels_shoes, class_names)


# === ANÁLISIS DE SUBCLUSTERS ===
def analyze_subclusters(subcluster_labels, original_labels, class_names):
    unique_subclusters = np.unique(subcluster_labels)

    print("\n=== ANÁLISIS DETALLADO DE SUBCLUSTERS ===")

    for cluster_id in unique_subclusters:
        if cluster_id == -1:
            print(f"\n🔍 Puntos de ruido: {np.sum(subcluster_labels == -1)}")
            continue

        cluster_mask = (subcluster_labels == cluster_id)
        cluster_original_labels = original_labels[cluster_mask]

        unique_classes, class_counts = np.unique(cluster_original_labels, return_counts=True)
        total_in_cluster = len(cluster_original_labels)
        dominant_class = unique_classes[np.argmax(class_counts)]
        dominant_percentage = (np.max(class_counts) / total_in_cluster) * 100

        print(f"\n📊 Subcluster {cluster_id}:")
        print(f"   - Total de imágenes: {total_in_cluster}")
        print(f"   - Clase dominante: {class_names[dominant_class]} ({dominant_percentage:.1f}%)")
        print(f"   - Distribución completa:")
        for class_id, count in zip(unique_classes, class_counts):
            percentage = (count / total_in_cluster) * 100
            print(f"       {class_names[class_id]}: {count} ({percentage:.1f}%)")


analyze_subclusters(subcluster_labels, labels_shoes, class_names)


# === MOSTRAR IMÁGENES REPRESENTATIVAS ===
def display_representative_images(images, labels, subcluster_labels, class_names,
                                  original_indices, max_images_per_cluster=5):
    unique_subclusters = np.unique(subcluster_labels)

    for cluster_id in unique_subclusters:
        if cluster_id == -1:
            continue

        cluster_mask = (subcluster_labels == cluster_id)
        cluster_images = images[original_indices[cluster_mask]]
        cluster_labels_sub = labels[cluster_mask]

        print(f"\n🖼️ Subcluster {cluster_id}: {len(cluster_images)} imágenes")

        # Mostrar imágenes representativas
        n_images = min(max_images_per_cluster, len(cluster_images))
        fig, axes = plt.subplots(1, n_images, figsize=(15, 3))

        if n_images == 1:
            axes = [axes]

        for i in range(n_images):
            axes[i].imshow(cluster_images[i], cmap='gray')
            axes[i].set_title(f'{class_names[cluster_labels_sub[i]]}')
            axes[i].axis('off')

        plt.suptitle(f'Subcluster {cluster_id} - Imágenes Representativas', fontsize=14)
        plt.tight_layout()
        plt.show()


# Mostrar imágenes representativas
display_representative_images(images, labels, subcluster_labels, class_names, shoe_indices)

print("\n✅ Análisis completado con UMAP!")