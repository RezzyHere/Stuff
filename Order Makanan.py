import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

def create_form():
    form = QWidget()
    form.setWindowTitle("Menu Restoran")
    label_makanan = QLabel("Menu Makanan:\n1.Nasi Goreng \n2.Mi Goreng \n3.Soto Ayam")
    label_minuman = QLabel("Menu Minuman:\n1.Air Mineral\n2.Teh Manis")
    label_food = QLabel("Makanan:")
    input_food = QLineEdit()
    
    label_drink = QLabel("Minuman:")
    input_drink = QLineEdit()
    
    submit_order = QPushButton("Order")
    
    def simpan_order():
        food = input_food.text()
        drink = input_drink.text()
        
        if not food or not drink:
            QMessageBox.warning(form, "Peringatan", "Semua kolom harus diisi")
            return
        
        QMessageBox.information(form, "Sukses", f"Orderan diterima!\nMakanan: {food}\nMinuman: {drink}")
    
    submit_order.clicked.connect(simpan_order)
    
    layout = QVBoxLayout()
    layout.addWidget(label_makanan)
    layout.addWidget(label_minuman)
    layout.addWidget(label_food)
    layout.addWidget(input_food)
    layout.addWidget(label_drink)
    layout.addWidget(input_drink)
    layout.addWidget(submit_order)
    
    form.setLayout(layout)
    form.show()
    
    return form

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = create_form()
    sys.exit(app.exec_())