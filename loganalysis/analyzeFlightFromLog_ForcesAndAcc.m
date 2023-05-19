% Load the ULog Files
ulog_obj= ulogreader("Ulog-files/TestDatenKönig/log_111_2023-4-14-15-19-36.ulg");
tmp = ulog_obj.readTopicMsgs(); % Just for viewing the values manually

veh_glob_position = ulog_obj.readTopicMsgs("TopicNames","vehicle_global_position").TopicMessages{1, 1};
actuators_output = ulog_obj.readTopicMsgs("TopicNames","actuator_outputs").TopicMessages{1, 1}.output;
veh_acc = ulog_obj.readTopicMsgs("TopicNames","vehicle_acceleration").TopicMessages{1, 1};
ang_acc = ulog_obj.readTopicMsgs("TopicNames","vehicle_angular_acceleration").TopicMessages{1, 1};

subplot(2, 1, 1)
lin_plot = plot(veh_acc.timestamp_sample, veh_acc.xyz);
title("Vehicle accleration")
xlabel("Time")
ylabel("Acceleration [m/s]")
max_i = find(veh_acc.xyz == max(veh_acc.xyz));
datatip(lin_plot(1), "DataIndex", max_i(1), "Location","northwest");
datatip(lin_plot(2), "DataIndex", max_i(2), "Location","northwest");
datatip(lin_plot(3), "DataIndex", max_i(3), "Location","southwest");

subplot(2, 1, 2)
ang_plot = plot(ang_acc.timestamp_sample, ang_acc.xyz);
title("Angular acceleration")
xlabel("Time")
ylabel("Angluar acceleration [rad/s]")
max_i = find(abs(ang_acc.xyz) == max(abs(ang_acc.xyz)));
datatip(ang_plot(1), "DataIndex", max_i(1), "Location","northwest");
datatip(ang_plot(2), "DataIndex", max_i(2), "Location","northwest");
datatip(ang_plot(3), "DataIndex", max_i(3), "Location","northwest");

