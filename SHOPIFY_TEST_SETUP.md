# Shopify Partners Test Setup for Unmuted

## 🧪 Quick Test Setup (No Payment Required)

### **Step 1: Create Shopify Partners Account**

1. Go to [shopify.com/partners](https://www.shopify.com/partners)
2. Sign up for free (no credit card needed)
3. Click **Stores** → **Add store** → **Development store**
4. Fill in:
   - Store name: `unmuted-test` (or whatever you want)
   - Store purpose: "Test store for client"
   - Build for: "Myself or my company"
5. Click **Create development store**

✅ **This is completely free and never expires!**

---

### **Step 2: Add Test Products (5 minutes)**

1. In your development store admin, go to **Products** → **Add product**
2. Create 1-2 simple test products:
   - **Product 1:** "Unmuted T-Shirt"
     - Price: $25
     - Add a placeholder image (any image works for testing)
   - **Product 2:** "Unmuted Hoodie"  
     - Price: $45
     - Add a placeholder image

Don't worry about perfect details - this is just for testing!

---

### **Step 3: Enable Buy Button Channel**

1. In Shopify admin → **Sales channels** (left sidebar)
2. Click **+** next to "Sales channels"
3. Search for **"Buy Button"**
4. Click **Add channel**
5. Click **Create a Buy Button**

---

### **Step 4: Generate Buy Button for Test Product**

1. Click **Create a Buy Button** → **Product**
2. Select your test product (e.g., "Unmuted T-Shirt")
3. Customize appearance:
   - **Button style:** Choose what looks good
   - **Button text:** "Add to Cart" or "Buy Now"
4. Click **Next**
5. **Copy the embed code** (the entire `<div>` and `<script>` block)

---

### **Step 5: Add to Your Site**

1. Open `/Users/adrianaso/Documents/unmuted/templates/shop.html`
2. Find line 23: `<!-- OPTION 1: Individual Product Buy Buttons -->`
3. Paste your Shopify embed code right below it
4. Save the file

---

### **Step 6: Test Locally**

```bash
# Build the site
python3 site.py build

# Start local server
python3 -m http.server 8000 --directory docs

# Open in browser
# Go to: http://localhost:8000/shop.html
```

You should see your test product with a working "Add to Cart" button!

---

### **Step 7: Push to GitHub (Make it Live)**

```bash
git add -A
git commit -m "Add Shopify test product"
git push origin main
```

Wait 1-2 minutes, then visit: `https://adrianaso123.github.io/unmuted/shop.html`

---

## 🔄 **Testing Workflow:**

### **When you make changes to Shopify:**
1. Update product in Shopify admin
2. Changes appear automatically (Buy Button pulls live data)
3. No need to rebuild your site!

### **When you make changes to your site:**
1. Edit files locally
2. Run `python3 site.py build`
3. Test at `http://localhost:8000`
4. Push to GitHub: `git add -A && git commit -m "Update" && git push`

---

## 📝 **Quick Reference:**

### **Your Development Store:**
- URL: `https://unmuted-test.myshopify.com` (or whatever you named it)
- Admin: `https://unmuted-test.myshopify.com/admin`

### **Test Checkout:**
- Use Shopify's test credit card: `1` (Bogus Gateway)
- Or: `4242 4242 4242 4242` (any future expiry, any CVV)

### **Files You'll Edit:**
- **Add products:** `/templates/shop.html` (paste Buy Button code)
- **Link to store:** `/content/config.yaml` (add store URL)

---

## 🎨 **Customizing Buy Button Colors:**

To match your site's pink/coral theme, add this to the Buy Button code:

```javascript
styles: {
  button: {
    'font-family': 'DM Sans, sans-serif',
    'background-color': '#ec4899',  // Your pink color
    ':hover': {
      'background-color': '#db2777'  // Darker pink on hover
    },
    'border-radius': '8px',
    'padding': '16px 32px'
  }
}
```

---

## ✅ **What This Gets You:**

- ✅ Free development store (no payment, no expiry)
- ✅ Test products you can update anytime
- ✅ Working checkout (test mode)
- ✅ Real-time updates (Shopify changes appear instantly)
- ✅ Full e-commerce testing without logistics setup

---

## 🚀 **Next Steps After Testing:**

1. When ready for real products:
   - Keep using the same development store
   - Add real product photos and descriptions
   - Set up real payment processing
   - Remove test mode

2. Or create a new production store:
   - Transfer products from dev store
   - Set up custom domain
   - Enable real payments

---

## 💡 **Pro Tips:**

1. **Multiple Products:** Create multiple Buy Buttons and paste them all in `shop.html`
2. **Collections:** Use Collection Buy Button to show all products at once
3. **Styling:** The Buy Button is responsive and matches your site automatically
4. **Testing:** Use Shopify's Bogus Gateway for test purchases (no real money)

---

## 🆘 **Troubleshooting:**

**Buy Button not showing?**
- Check browser console for errors
- Make sure you copied the entire embed code (both `<div>` and `<script>`)
- Try hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+F5 (Windows)

**Changes not appearing on GitHub Pages?**
- Wait 1-2 minutes for GitHub to rebuild
- Clear browser cache
- Check that you pushed to `main` branch

**Need to update product?**
- Just edit in Shopify admin
- Changes appear automatically (no rebuild needed!)
