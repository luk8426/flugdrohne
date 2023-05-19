% Load the ULog Files
ulog_obj= ulogreader("Ulog-files/TestDatenKönig/log_111_2023-4-14-15-19-36.ulg");
tmp = ulog_obj.readTopicMsgs(); % Just for viewing the values manually

veh_glob_position = ulog_obj.readTopicMsgs("TopicNames","vehicle_global_position").TopicMessages{1, 1};
actuators_output = ulog_obj.readTopicMsgs("TopicNames","actuator_outputs").TopicMessages{1, 1}.output;
veh_acc = ulog_obj.readTopicMsgs("TopicNames","vehicle_acceleration").TopicMessages{1, 1};
ang_acc = ulog_obj.readTopicMsgs("TopicNames","vehicle_angular_acceleration").TopicMessages{1, 1};

subplot(3, 1, 1)
lin_plot = plot(veh_acc.timestamp_sample, veh_acc.xyz);
title("Vehicle accleration")
xlabel("Time")
ylabel("Acceleration [m/s^2]")
legend("x", "y", "z")
max_i = 1:3;
for i = 1:3
    max_i(i) = find(abs(veh_acc.xyz(:,i)) == max(abs(veh_acc.xyz(:,i))));
end
datatip(lin_plot(1), "DataIndex", max_i(1), "Location","southeast");
datatip(lin_plot(2), "DataIndex", max_i(2), "Location","southwest");
datatip(lin_plot(3), "DataIndex", max_i(3), "Location","southwest");

subplot(3, 1, 2)
ang_plot = plot(ang_acc.timestamp_sample, ang_acc.xyz);
title("Angular acceleration")
xlabel("Time")
ylabel("Angluar acceleration [rad/s^2]")
legend("x", "y", "z")
for i = 1:3
    max_i(i) = find(abs(ang_acc.xyz(:,i)) == max(abs(ang_acc.xyz(:,i))));
end
datatip(ang_plot(1), "DataIndex", max_i(1), "Location","northwest");
datatip(ang_plot(2), "DataIndex", max_i(2), "Location","northwest");
datatip(ang_plot(3), "DataIndex", max_i(3), "Location","northwest");

subplot(3, 1, 3)
jerk = gradient(veh_acc.xyz);
jerk_plot = plot(veh_acc.timestamp_sample, jerk);
title("Jerk of lateral acceleration")
xlabel("Time")
ylabel("Jerk in m/s^3")
legend("x", "y", "z");
for i = 1:3
    max_i(i) = find(abs(jerk(:,i)) == max(abs(jerk(:,i))));
end
datatip(jerk_plot(1), "DataIndex", max_i(1), "Location","northwest");
datatip(jerk_plot(2), "DataIndex", max_i(2), "Location","northwest");
datatip(jerk_plot(3), "DataIndex", max_i(3), "Location","southwest");
