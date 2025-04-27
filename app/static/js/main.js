document.addEventListener('DOMContentLoaded', function () {
    mataflash();
});
document.addEventListener('DOMContentLoaded', function () {
    moedado();
});
function moedado(){
    
}
function mataflash() {
    var flashMessage = document.querySelector('.flash');
    if (flashMessage) {
        setTimeout(function () {
            flashMessage.style.display = 'none';
        }, 2000);
    }
}
function show_div(e){
    console.log(e)
    div_login = document.getElementById('div_login')
    caixa_div_login = document.getElementById('caixa_div_login')
    div_criar_conta = document.getElementById('div_criar_conta')
    caixa_div_criar_conta = document.getElementById('caixa_div_criar_conta')
    logoff = document.getElementById('div_logoff')
    quadro_pesquisa = document.getElementById('aside_pesquisa')

    if(e.id == 'logoff'){
        logoff.style.display = 'block'
    }
    if(e.id == 'login_pessoinha'){
        caixa_div_login.style.display = 'flex'

    }
    if(e.id == 'fake_link_criar_conta' || e.id == 'falso_button'){
        caixa_div_login.style.display = 'none'
        caixa_div_criar_conta.style.display = 'block'
    }
    if(e.id == 'setinha'){
        quadro_pesquisa.classList.toggle("aberta");
        e.classList.toggle("active")
         
    }

}
    function fechar(e){
        const div_pai = e.parentNode
        const div_avo = div_pai.parentNode
        div_avo.style.display = 'none'
        console.log(div_avo)

    }
    function closer(id){
        var alvo = document.getElementById(id)
        alvo.style.display = 'none'
    }
    let currentIndex = 0;
    let totalItems = document.querySelectorAll('.carousel-item').length;
    const carousel = document.getElementById('carousel');
    
    function showSlide(index) {
      currentIndex = (index + totalItems) % totalItems;
      const translateValue = -currentIndex * 100 + '%';
      carousel.style.transform = 'translateX(' + translateValue + ')';
    }
    
    function changeSlide(offset) {
      showSlide(currentIndex + offset);
}
    
    function updateTotalItems() {
      const updatedTotalItems = document.querySelectorAll('.carousel-item').length;
    
      if (updatedTotalItems !== totalItems) {
        currentIndex = 0;
        totalItems = updatedTotalItems;
        showSlide(currentIndex);
      }
}
    

    function aparece_valor(e){
        var p = document.getElementById(`valor_${e.name}`)
        var input_inicio = parseInt(document.getElementById(`select_${e.classList[1]}_inicio`).value)
        var input_fim = parseInt(document.getElementById(`select_${e.classList[1]}_fim`).value)
        var categoria = e.classList[1] // quilometro ou preco

        if(p.classList[1] == 'preco'){ p.innerText = moedinha(parseInt(e.value)) }
        if(p.classList[1] == 'quilometro'){ p.innerText =  numerinho(parseInt(e.value))+' KM' }
        
        if(input_inicio > input_fim){
            var p = document.getElementById(`valor_select_${categoria}_fim`)
            document.getElementById(`select_${categoria}_fim`).value = input_inicio
            if(p.classList[1] == 'preco'){p.innerText = moedinha(parseInt(e.value)) }
            if(p.classList[1] == 'quilometro'){p.innerText =  numerinho(parseInt(e.value))+' KM'}
        }
        function att_valor(){
            if(p.classList[1] == 'preco'){ p.innerText = moedinha(parseInt(e.value)) }
            if(p.classList[1] == 'quilometro'){ p.innerText =  numerinho(parseInt(e.value))+' KM' }
        }
    }
    function moedinha(numero) {
    if (typeof numero === 'number' && !isNaN(numero)) {
        let numeroFormatado = numero.toFixed(2);
        let [parteInteira, parteDecimal] = numeroFormatado.split('.');
        parteInteira = parseInt(parteInteira).toLocaleString('pt-BR');
        let valorFormatado = `R$${parteInteira},${parteDecimal}`;
        return valorFormatado;
    } else {
        return 'Erro: Valor não é um número';
    }
}
    function numerinho(numero) {
    return numero.toLocaleString('pt-BR')
}

    updateTotalItems();


    
    const fileInput = document.querySelector(".fileInput");
    const pictureImage = document.querySelector(".picture_image");
    const uploadFile = (files) => {
        const API_ENDPOINT = `/processar_midia?origem=${fileInput.classList[1]}&id=${fileInput.classList[2]}&nome=${fileInput.classList[3]}`;
        const request = new XMLHttpRequest();
        const formData = new FormData();
      
        request.open("POST", API_ENDPOINT, true);
        request.onreadystatechange = () => {
          if (request.readyState === 4 && request.status === 200) {
          }
        };
        request.getAllResponseHeaders()
        for (let i = 0; i < files.length; i++) {
          formData.append(`${files[i].name}`, files[i])
          formData.append('size',files[0].size)
        }
        request.send(formData);
      };
      if(fileInput){
          fileInput.addEventListener("change", event => {
            const files = event.target.files;
            const ler = new FileReader()
            ler.readAsDataURL(files[0])
            ler.addEventListener("load", function (e) {
                const readerTarget = e.target;
                const tipo = e.target.result.substring(5, 10)
                if(tipo == 'image'){
                    const img = document.createElement("img");
                    const img_text = document.createElement("p")
                    img_text.innerText = `${files[0].name} ${(files[0].size/1000000).toFixed(2)}Mb`
                    img.src = readerTarget.result;
                    img.classList.add("img");
                    pictureImage.appendChild(img);
                    pictureImage.appendChild(img_text)
                }
                if(tipo == 'video'){
                    const video = document.createElement("video");
                    const video_text = document.createElement("p");
                    video_text.innerText = `${files[0].name} ${(files[0].size/1000000).toFixed(2)}Mb`;
                    const reader = new FileReader();
                    reader.onload = function(event) {
                        video.src = event.target.result;
                        video.classList.add("video");
                        video.setAttribute("controls", "");
                        pictureImage.appendChild(video);
                        pictureImage.appendChild(video_text);
                    };
                    
                    reader.readAsDataURL(files[0]);
                }
        });
            uploadFile(files);
          });
      }



      
      function toggleFullScreen(e) {
        var elem = document.getElementById(e.id);
        console.log(e.id)
        if (elem.requestFullscreen) {
            elem.requestFullscreen();
        } else if (elem.mozRequestFullScreen) {
            elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullscreen) { 
            elem.webkitRequestFullscreen();
        } else if (elem.msRequestFullscreen) {
            elem.msRequestFullscreen();
        }
    }


