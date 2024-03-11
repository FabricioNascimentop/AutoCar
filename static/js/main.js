document.addEventListener('DOMContentLoaded', function () {
    mataflash();
});
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
    caixa_div_login = document.getElementById('caixa_div_login')
    div_criar_conta = document.getElementById('div_criar_conta')
    caixa_div_criar_conta = document.getElementById('caixa_div_criar_conta')
    

    if(e.id == 'login_pessoinha'){
        caixa_div_login.style.display = 'block'

    }
    if(e.id == 'fake_link_criar_conta'){
        caixa_div_login.style.display = 'none'
        caixa_div_criar_conta.style.display = 'block'
    }


}
    function fechar(e){
        const div_pai = e.parentNode
        const div_avo = div_pai.parentNode
        div_avo.style.display = 'none'

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