clc;
clear;
close all;

data = readtable('comparison_log.csv');

t = data.time_s;

% Position errors
odom_error = hypot(data.gt_x-data.odom_x, ...
                   data.gt_y-data.odom_y);

ekf_error = hypot(data.gt_x-data.ekf_x, ...
                  data.gt_y-data.ekf_y);

% 1. Robot trajectory
figure;
plot(data.gt_x,data.gt_y,'k','LineWidth',1.5);
hold on;
plot(data.odom_x,data.odom_y,'b--');
plot(data.ekf_x,data.ekf_y,'r:');
xlabel('X Position (m)');
ylabel('Y Position (m)');
title('Robot Trajectory Comparison');
legend('Ground Truth','Wheel Odometry','EKF');
grid on;
saveas(gcf,'trajectory_comparison.png');

% 2. Localization error
figure;
plot(t,odom_error,'b');
hold on;
plot(t,ekf_error,'r');
xlabel('Time (s)');
ylabel('Position Error (m)');
title('Localization Error Comparison');
legend('Wheel Odometry','EKF');
grid on;
saveas(gcf,'localization_error.png');

% 3. Linear velocity
figure;
plot(t,data.linear_velocity,'LineWidth',1.2);
xlabel('Time (s)');
ylabel('Linear Velocity (m/s)');
title('Robot Linear Velocity');
grid on;
saveas(gcf,'linear_velocity.png');

% 4. Angular velocity
figure;
plot(t,data.angular_velocity,'LineWidth',1.2);
xlabel('Time (s)');
ylabel('Angular Velocity (rad/s)');
title('Robot Angular Velocity');
grid on;
saveas(gcf,'angular_velocity.png');

% 5. Obstacle distance
figure;
plot(t,data.nearest_obstacle,'LineWidth',1.2);
xlabel('Time (s)');
ylabel('Distance (m)');
title('LiDAR Obstacle Distance');
grid on;
saveas(gcf,'obstacle_distance.png');

disp('All five graphs generated successfully.');
