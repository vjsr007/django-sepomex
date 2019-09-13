(() => {
    "use strict";

    const urlModel = 'http://127.0.0.1:5500/digits/model.json';
    const urlTestData = 'http://127.0.0.1:5500/digits/input/test.csv';
    let model = {};
    let data = {};

    const CLASS_NUMBERS = [0,1,2,3,4,5,6,7,8,9]

    const loadModel = () => {
        return tf.loadLayersModel(urlModel);
    }

    const loadTestData = () => {
        return new Promise((resolved, rejected) => {
            try {
                Papa.parse(urlTestData, {
                    download: true,
                    complete: function(results) {
                        resolved(results.data);
                    }
                });
            }
            catch(ex){
                rejected(ex);
            }
        });  
    }

    const zeroFill = (number,width) => {
      width -= number.toString().length;
      if ( width > 0 )
      {
        return new Array( width + (/\./.test( number ) ? 2 : 1) ).join( '0' ) + number;
      }
      return number + ""; // always return a string
    }

    const setupCanvas = () => {
        const c = document.getElementById("myCanvas");
        const ctx = c.getContext("2d");
        const index = parseInt(Math.random() * data.length);
        const pixels = data[index];

        console.log(index);
        console.log(data[index])

        const image = [];
        pixels.forEach((item, idx) => {
            const arrayY = [];
            const arrayX = [];
            const y = parseInt(idx/28);
            const x = parseInt(idx - (y*28));
            image.push(parseInt(item));
            ctx.fillStyle = `#${zeroFill(parseInt(item).toString(16), 6)}`;
            ctx.fillRect( x, y, 1, 1 );
        });

        return image;
    }

    const predictCanvas = (image) => {
        const c = document.getElementById("myCanvas");
        const ctx = c.getContext("2d");

        const example = tf.tensor(image, [1,28,28,1]);
        const prediction = model.predict(example);
        const result = prediction.dataSync();
        console.log(result);
        console.log(CLASS_NUMBERS[result.indexOf(1)]);

        return CLASS_NUMBERS[result.indexOf(1)]
    }

    return (async () => {
        model = await loadModel();
        data = await loadTestData();
        const image = setupCanvas();
        const number = predictCanvas(image);

        document.getElementsByTagName("h3")[0].innerHTML = number;
    });

})()();
