import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")
FRONTEND_FILE = os.path.join(BASE_DIR, "product.html")

def generate_card(item):
    img_url = item.get('image', 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400')
    
    return f"""
    <div class="product-card flex flex-col justify-between h-[400px] text-center group">
        <div>
            <h3 class="text-lg font-black uppercase italic tracking-tighter text-white">{item['name']}</h3>
            <p class="text-[#c3f5ff] font-bold text-sm mt-1">${item['price']}</p>
        </div>
        
        <div class="flex-1 flex items-center justify-center py-4">
             <img src="{img_url}" class="shoe-img h-40 object-contain transition-transform group-hover:scale-110" alt="{item['name']}">
        </div>
        
        <div class="flex flex-col items-center gap-3">
            <p class="text-[9px] text-gray-400 px-4 line-clamp-2 opacity-0 group-hover:opacity-100 transition-opacity uppercase font-medium">
                {item.get('detail', 'Premium Quality Gear')}
            </p>
            <button onclick="addToCart({item['id']}, '{item['name']}', {item['price']})" 
                class="w-full py-4 bg-[#c3f5ff] text-black font-black rounded-2xl text-[10px] uppercase tracking-widest hover:bg-white transition-all shadow-lg active:scale-95">
                Add to Cart
            </button>
        </div>
    </div>
    """

def sync_store():
    try:
        if not os.path.exists(DATA_FILE):
            print(f"Error: {DATA_FILE} not found!")
            return
        
        if not os.path.exists(FRONTEND_FILE):
            print(f"Error: {FRONTEND_FILE} not found!")
            return

        with open(DATA_FILE, "r", encoding="utf-8") as f:
            items = json.load(f)

        with open(FRONTEND_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        cards_html = "\n".join([generate_card(i) for i in items])
        
        START = ""
        END = ""
        
        start_idx = content.find(START)
        end_idx = content.find(END)

        if start_idx == -1 or end_idx == -1:
            print("Error: PRODUCTS_START or END comments not found in HTML file!")
            return

        new_content = (
            content[:start_idx + len(START)] + 
            "\n" + cards_html + "\n" + 
            content[end_idx:]
        )
        
        with open(FRONTEND_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print(f"Success: {len(items)} products synced. No duplicates found!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    sync_store()