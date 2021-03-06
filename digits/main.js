(() => {
    "use strict";

    const urlModel = 'http://127.0.0.1:5500/digits/model.json';
    const urlTestData = 'http://127.0.0.1:5500/digits/input/test.csv';
    let model = {};
    let data = {};

    const CLASS_NUMBERS = [0,1,2,3,4,5,6,7,8,9];
    const WIDTH = 28;
    const HEIGHT = 28;

    let canvas, ctx, 
    flag = false,
    prevX = 0,
    currX = 0,
    prevY = 0,
    currY = 0,
    dot_flag = false;
    
    var x = "blue",
    y = 1;   

    const loadModel = () => {
        return tf.loadLayersModel(urlModel);
    };

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
    };

    const zeroFill = (number,width) => {
      width -= number.toString().length;
      if ( width > 0 )
      {
        return new Array( width + (/\./.test( number ) ? 2 : 1) ).join( '0' ) + number;
      }
      return number + ""; // always return a string
    };

    const erase = () => {
        ctx.clearRect(0, 0, WIDTH, HEIGHT);
    };

    const save = async () => {
        const imageData = ctx.getImageData(0, 0, 28, 28).data;

        // console.log(imageData);

        const image = [];
        for(let i=0; i<imageData.length; i++) {
            const pixel = imageData[i + 2];
            image.push(pixel);
            i+=3;
        }

        const number = predictCanvas(image);

        document.getElementsByTagName("h3")[0].innerHTML = number;
    };

    const draw = () => {
        ctx.beginPath();
        ctx.moveTo(prevX, prevY);
        ctx.lineTo(currX, currY);
        ctx.strokeStyle = x;
        ctx.lineWidth = y;
        ctx.stroke();
        ctx.closePath();
    };

    const findxy = (res, e) => {
        if (res == 'down') {
            erase();
            prevX = currX;
            prevY = currY;
            currX = e.clientX - canvas.offsetLeft;
            currY = e.clientY - canvas.offsetTop;
    
            flag = true;
            dot_flag = true;
            if (dot_flag) {
                ctx.beginPath();
                ctx.fillStyle = x;
                ctx.fillRect(currX, currY, 2, 2);
                ctx.closePath();
                dot_flag = false;
            }
        }
        if (res == 'up' || res == "out") {
            flag = false;
            save();
        }
        if (res == 'move') {
            if (flag) {
                prevX = currX;
                prevY = currY;
                currX = e.clientX - canvas.offsetLeft;
                currY = e.clientY - canvas.offsetTop;
                draw();
            }
        }
    };

    const getRandomData = (idx) => {
        const image = [];
            
        const index = idx ? idx : parseInt(Math.random() * data.length);
        const pixels = data[index];

        // console.log(index);
        // console.log(data[index])

        pixels.forEach((item, idx) => {
            const y = parseInt(idx/28);
            const x = parseInt(idx - (y*28));
            image.push(parseInt(item));
            ctx.fillStyle = `#${zeroFill(parseInt(item).toString(16), 6)}`;
            ctx.fillRect( x, y, 1, 1 );
        });

        return image;
    };

    const setupCanvas = () => {
        canvas = document.getElementById("myCanvas");
        ctx = canvas.getContext("2d");

        canvas.addEventListener("mousemove", (e) => {
            findxy('move', e);
        }, false);
        canvas.addEventListener("mousedown", (e) => {
            findxy('down', e);
        }, false);
        canvas.addEventListener("mouseup", (e) => {
            findxy('up', e);
        }, false);
        canvas.addEventListener("mouseout", (e) => {
            findxy('out', e);
        }, false);

    };

    const predictCanvas = (image) => {
        canvas = document.getElementById("myCanvas");
        ctx = canvas.getContext("2d");

        const example = tf.tensor(image, [1,WIDTH,HEIGHT,1]);
        const prediction = model.predict(example);
        const result = prediction.dataSync();
        console.log(result);
        console.log(tf.memory());
        //console.log(CLASS_NUMBERS[result.indexOf(1)]);

        return CLASS_NUMBERS[result.indexOf(1)];
    };

    return (async () => {
        model = await loadModel();     
        setupCanvas();

        //data = await loadTestData();
        //const image = getRandomData();   
        //const number = predictCanvas(image);
        //document.getElementsByTagName("h3")[0].innerHTML = number;
    });

})()();
