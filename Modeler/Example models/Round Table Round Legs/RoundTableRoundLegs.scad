union(){
    cube(size=[0, 0, 0]);
    translate(v=[0, 0, 100]){
        color(""){
            cylinder(h=10, r=100);
        };
    };
    translate(v=[80, 0, 0]){
        color(""){
            cylinder(h=100, r=10);
        };
    };
    translate(v=[0, 80, 0]){
        color(""){
            cylinder(h=100, r=10);
        };
    };
    translate(v=[-80, 0, 0]){
        color(""){
            cylinder(h=100, r=10);
        };
    };
    translate(v=[0, -80, 0]){
        color(""){
            cylinder(h=100, r=10);
        };
    };
};
