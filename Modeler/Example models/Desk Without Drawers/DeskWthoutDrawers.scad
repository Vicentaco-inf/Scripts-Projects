union(){
    cube(size=[0, 0, 0]);
    translate(v=[-50, -100, 100]){
        color(""){
            cube(size=[100, 200, 10]);
        };
    };
    translate(v=[-50, -100, 50]){
        cube(size=[1, 200, 50]);
    };
    translate(v=[-50, 99, 0]){
        cube(size=[100, 1, 100]);
    };
    translate(v=[-50, -100, 0]){
        cube(size=[100, 1, 100]);
    };
};
