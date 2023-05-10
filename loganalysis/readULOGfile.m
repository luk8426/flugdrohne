% Load the ULog Files
ulogOBJ_wo_load = ulogreader("Ulog-files/log_110_2023-4-14-14-58-44.ulg");
acc_wo_load = ulogOBJ_wo_load.readTopicMsgs("TopicNames","vehicle_acceleration").TopicMessages{1, 1};
ulogOBJ_with_load = ulogreader("Ulog-files/log_111_2023-4-14-15-19-36.ulg");
tmp = ulogOBJ_with_load.readTopicMsgs();
acc_with_load = ulogOBJ_with_load.readTopicMsgs("TopicNames","vehicle_acceleration").TopicMessages{1, 1};

max_xyz_angular_velo_w_load = max(ulogOBJ_with_load.readTopicMsgs("TopicNames","vehicle_angular_acceleration").TopicMessages{1, 1}.xyz);
max_xyz_angular_velo_wo_load = max(ulogOBJ_wo_load.readTopicMsgs("TopicNames","vehicle_angular_acceleration").TopicMessages{1, 1}.xyz);

delta_xyz = acc_with_load.xyz(1:4000, :) - acc_wo_load.xyz(1:4000, :);
subplot(3, 1, 1)
plot(acc_with_load.xyz(1:4000, :))
subplot(3, 1, 2);
plot(acc_wo_load.xyz(1:4000, :));
subplot(3, 1, 3)
plot(delta_xyz)