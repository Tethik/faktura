class Breadcrumb:
    def __init__(self, url, text):
        self.url = url
        self.text = text

url_dict = {
    'Main Menu': '/',
    'Invoices': '/invoices',
    'Customers': '/customers',
    'Settings': '/settings'
}

def breadcrumbs(*shortwords):
    return [Breadcrumb(url_dict[word], word) for word in shortwords]
