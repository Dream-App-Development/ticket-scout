import json

from fastapi import FastAPI

app = FastAPI(
    prefix="/tickets",
    tags=["Tickets"],
)


@app.get("/")
def execute_request(self, url, method, data=None):
    data_str = json.dumps(data) if data else None
    print(url, method, data_str)
    # JavaScript function to perform the XHR request
    js_script = """
                  (params) => {
                      return new Promise((resolve, reject) => {
                          var xhr = new XMLHttpRequest();
                          xhr.onreadystatechange = function () {
                              if (xhr.readyState === 4) {
                                  resolve({status: xhr.status, responseText: xhr.responseText});
                              }
                          };
                          xhr.open(params.method, params.url, true);
                          xhr.setRequestHeader('Content-Type', 'application/json');
                          xhr.send(params.data);
                      });
                  }
              """
    # Pack the parameters into a single object
    params = {
        'url': url,
        'method': method,
        'data': data_str,
    }
    # Execute the script with the parameters object
    response = self.page.evaluate(js_script, params)
    print("response:", type(response), response.get("status"))
    return response.get("responseText")
