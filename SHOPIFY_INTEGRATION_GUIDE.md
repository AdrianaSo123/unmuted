# Shopify Integration Guide for Unmuted

## 🛍️ Three Ways to Connect Shopify

### **Option 1: Shopify Buy Button (Recommended - Easiest)**

Embed individual products or collections directly on your shop page.

#### Steps:
1. **Create Buy Button in Shopify:**
   - Go to Shopify Admin → **Sales channels** → **Online Store**
   - Click **Themes** → **Customize**
   - Go to **App embeds** → Enable **Buy Button** channel
   
2. **Generate Product Buy Button:**
   - Go to **Products** → Select a product
   - Click **More actions** → **Create Buy Button**
   - Customize appearance (colors, button text, etc.)
   - Copy the embed code

3. **Add to Your Site:**
   - Open `/Users/adrianaso/Documents/unmuted/templates/shop.html`
   - Find the comment: `<!-- OPTION 1: Individual Product Buy Buttons -->`
   - Paste your Shopify embed code below it
   - Build and push: `python3 site.py build && git add -A && git commit -m "Add Shopify products" && git push`

#### Example Embed Code:
```html
<!-- OPTION 1: Individual Product Buy Buttons -->
<div id='product-component-1234567890'></div>
<script type="text/javascript">
/*<![CDATA[*/
(function () {
  var scriptURL = 'https://sdks.shopifycdn.com/buy-button/latest/buy-button-storefront.min.js';
  if (window.ShopifyBuy) {
    if (window.ShopifyBuy.UI) {
      ShopifyBuyInit();
    } else {
      loadScript();
    }
  } else {
    loadScript();
  }
  function loadScript() {
    var script = document.createElement('script');
    script.async = true;
    script.src = scriptURL;
    (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(script);
    script.onload = ShopifyBuyInit;
  }
  function ShopifyBuyInit() {
    var client = ShopifyBuy.buildClient({
      domain: 'your-store.myshopify.com',
      storefrontAccessToken: 'your-storefront-access-token',
    });
    ShopifyBuy.UI.onReady(client).then(function (ui) {
      ui.createComponent('product', {
        id: 'your-product-id',
        node: document.getElementById('product-component-1234567890'),
        // Customize styling here
      });
    });
  }
})();
/*]]>*/
</script>
```

---

### **Option 2: Collection Buy Button**

Display an entire collection of products.

#### Steps:
1. **Create Collection:**
   - Shopify Admin → **Products** → **Collections**
   - Create a new collection (e.g., "Unmuted Merch")
   - Add products to it

2. **Generate Collection Buy Button:**
   - Go to the collection
   - Click **Create Buy Button**
   - Customize and copy embed code

3. **Add to Site:**
   - Open `/templates/shop.html`
   - Find: `<!-- OPTION 2: Collection Buy Button -->`
   - Paste embed code
   - Build and push

---

### **Option 3: Link to Full Shopify Store**

Simplest option - just link to your Shopify store.

#### Steps:
1. **Get Your Store URL:**
   - Your Shopify store URL (e.g., `https://unmuted.myshopify.com`)
   - Or custom domain if you have one

2. **Add to Config:**
   - Open `/content/config.yaml`
   - Find: `shopify_store_url: ""`
   - Add your URL: `shopify_store_url: "https://unmuted.myshopify.com"`

3. **Build and Push:**
   ```bash
   python3 site.py build
   git add -A
   git commit -m "Add Shopify store link"
   git push
   ```

The shop page will automatically show a "Shop Now" button linking to your store.

---

## 🎨 Customizing Buy Button Appearance

Match your site's design by customizing the Buy Button:

```javascript
ShopifyBuy.UI.onReady(client).then(function (ui) {
  ui.createComponent('product', {
    id: 'your-product-id',
    node: document.getElementById('product-component'),
    moneyFormat: '%24%7B%7Bamount%7D%7D',
    options: {
      product: {
        styles: {
          product: {
            '@media (min-width: 601px)': {
              'max-width': 'calc(25% - 20px)',
              'margin-left': '20px',
              'margin-bottom': '50px'
            }
          },
          button: {
            'font-family': 'DM Sans, sans-serif',
            'font-size': '16px',
            'padding-top': '16px',
            'padding-bottom': '16px',
            'background-color': '#ec4899',  // Your coral/pink color
            ':hover': {
              'background-color': '#db2777'
            }
          }
        }
      },
      cart: {
        styles: {
          button: {
            'font-family': 'DM Sans, sans-serif',
            'background-color': '#ec4899',
            ':hover': {
              'background-color': '#db2777'
            }
          }
        }
      }
    }
  });
});
```

---

## 📝 Quick Setup Checklist

- [ ] Set up Shopify store
- [ ] Create products/collections
- [ ] Enable Buy Button channel in Shopify
- [ ] Generate Buy Button embed code
- [ ] Paste code into `/templates/shop.html`
- [ ] OR add store URL to `/content/config.yaml`
- [ ] Build site: `python3 site.py build`
- [ ] Test locally: `python3 -m http.server 8000 --directory docs`
- [ ] Push to GitHub: `git add -A && git commit -m "Add Shopify" && git push`

---

## 🔗 Useful Links

- [Shopify Buy Button Documentation](https://help.shopify.com/en/manual/online-sales-channels/buy-button)
- [Buy Button SDK](https://shopify.github.io/buy-button-js/)
- [Shopify Developer Docs](https://shopify.dev/)

---

## 💡 Tips

1. **Start Simple:** Use Option 3 (link to store) first, then add Buy Buttons later
2. **Test Products:** Create a few test products before going live
3. **Match Branding:** Customize Buy Button colors to match your site (pink/coral #ec4899)
4. **Mobile Friendly:** Buy Buttons are responsive by default
5. **Analytics:** Shopify tracks all sales automatically

---

## 🆘 Need Help?

If you run into issues:
1. Check Shopify's Buy Button documentation
2. Verify your Storefront Access Token is correct
3. Make sure Buy Button channel is enabled in Shopify
4. Test the embed code on a simple HTML page first
