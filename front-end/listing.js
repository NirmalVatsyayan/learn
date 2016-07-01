var getProducts = function(load_url){

    var success = function() {
        var product = JSON.parse(xhr.responseText);
        console.log(product);
        
	
	    var main_div = document.getElementById("main_div");
	    for (var data in product.results){
		    var sub_div = document.createElement('div');
            
            var id_span = document.createElement('span');
            id_span.className='id';
		    id_span.innerHTML = innerHTML = product.results[data].id;
		    sub_div.appendChild(id_span);
            
            var br = document.createElement("br");
		    var url_span = document.createElement('span');
		    url_span.innerHTML = innerHTML = product.results[data].news_url;
		    sub_div.appendChild(url_span);
            sub_div.appendChild(br)
            
            var br = document.createElement("br");
		    var title_span = document.createElement('span');
		    title_span.innerHTML = product.results[data].title;
		    sub_div.appendChild(title_span);
            sub_div.appendChild(br)
            
            var br = document.createElement("br");
		    var source_span = document.createElement('span');
		    source_span.innerHTML = product.results[data].source;
		    sub_div.appendChild(source_span);
            sub_div.appendChild(br)

            var br = document.createElement("br");
		    var upvote_span = document.createElement('span');
		    upvote_span.innerHTML = product.results[data].upvote;
		    sub_div.appendChild(upvote_span);
            sub_div.appendChild(br)
            
            var br = document.createElement("br");
		    var comment_span = document.createElement('span');
		    comment_span.innerHTML = product.results[data].comment;
		    sub_div.appendChild(comment_span);
            
            var btn = document.createElement("BUTTON");
            btn.setAttribute("id", product.results[data].id);
		    var t = document.createTextNode("DELETE");
		    btn.addEventListener( 'click', function(){
		    	console.log(this.id);
                this.parentElement.remove();
                console.log("hiding display");
                var xhr = new XMLHttpRequest();
                var url = "http://localhost:8000/apis/deletenews/?news_id="+this.id;
                console.log(url)  ;              
                xhr.open("PATCH", url, true);
                xhr.setRequestHeader("Authorization", localStorage.getItem('token'));
                xhr.send();
                return url
            } );
            btn.appendChild(t);

		    sub_div.appendChild(btn);
            
            var br = document.createElement("br");
		    main_div.appendChild(sub_div);
		    main_div.appendChild(br);
            
	    }


	    var br = document.createElement("br");
	    main_div.appendChild(br);
        
        var nbtn = document.createElement("BUTTON");
        nbtn.value=product.next;
        console.log("setting next value "+nbtn.value);
        console.log(nbtn.value)
        var t = document.createTextNode("NEXT");
       
        nbtn.addEventListener('click',function(){
        	/*var xhr = new XMLHttpRequest();
        	var url = this.value;
        	xhr.open("GET", url, true);
        	xhr.setRequestHeader("Authorization", localStorage.getItem('token'));
        	xhr.send();
            
            myFunction1(this.value);*/
            console.log("?????????????"+pbtn.value);
                page2 = load_url.search("page=2");
                page3 = load_url.search("page=3");
                
                if (page2 > -1){
        	        window.location.href = "temp2.html";
                }
                else if (page3 == -1){
                    window.location.href = "temp.html";
                }

        });
        nbtn.appendChild(t);
        main_div.appendChild(nbtn);

        var br = document.createElement("br");
	    main_div.appendChild(br);

        var pbtn = document.createElement("BUTTON");
        pbtn.value= product.previous;
        console.log("setting previous value "+pbtn.value);
        var t = document.createTextNode("PREVIOUS");
        pbtn.addEventListener('click',function(){
        	/*var xhr = new XMLHttpRequest();
        	var url = this.value;
        	xhr.open("GET", url, true);
        	xhr.setRequestHeader("Authorization", localStorage.getItem('token'));
        	xhr.send();
            myFunction1(this.value);*/
            console.log("?????????????"+pbtn.value);

            
                page2 = load_url.search("page=2");
                page3 = load_url.search("page=3");
                if (page2 > -1){
        	        window.location.href = "listing.html";
                }
                else if (page3 > -1){
                    window.location.href = "temp.html";
                }
        });
        pbtn.appendChild(t);
        main_div.appendChild(pbtn);
        var br = document.createElement("br");
	    main_div.appendChild(br);
        

    }

console.log("Getting Products...");
xhr = new XMLHttpRequest();
xhr.open("GET", load_url);
xhr.setRequestHeader("Authorization", localStorage.getItem('token'));
xhr.addEventListener("load", success);
xhr.send();
};

function myFunction(){
  console.log("Getting Products...");
  window.addEventListener("load", getProducts("http://localhost:8000/apis/news/"));
}

function myFunction1(){
  console.log("Getting Products...");
  window.addEventListener("load", getProducts("http://localhost:8000/apis/news/?page=2"));
}

function myFunction2(){
  console.log("Getting Products...");
  window.addEventListener("load", getProducts("http://localhost:8000/apis/news/?page=3"));
}