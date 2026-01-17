clc; clear all; close all;

recurdyn_data = readmatrix('../RECURDYN/rec_data_fix_free_fall.csv');
matlab_data = load('mat_data.csv');

ee_title_txt = {'EE position X', 'EE position Y', 'EE position Z', 'EE orientation Roll', 'EE orientation Pitch', 'EE orientation Yaw'};

rec_data_FL = [recurdyn_data(:, 1:2), recurdyn_data(:, 3:26)];
rec_data_ML = [recurdyn_data(:, 1:2), recurdyn_data(:, 27:50)];
rec_data_RL = [recurdyn_data(:, 1:2), recurdyn_data(:, 51:74)];
rec_data_FR = [recurdyn_data(:, 1:2), recurdyn_data(:, 75:98)];
rec_data_MR = [recurdyn_data(:, 1:2), recurdyn_data(:, 99:122)];
rec_data_RR = [recurdyn_data(:, 1:2), recurdyn_data(:, 123:146)];

mat_data_FL = [matlab_data(:, 1:2), matlab_data(:, 3:26)];
mat_data_ML = [matlab_data(:, 1:2), matlab_data(:, 27:50)];
mat_data_RL = [matlab_data(:, 1:2), matlab_data(:, 51:74)];
mat_data_FR = [matlab_data(:, 1:2), matlab_data(:, 75:98)];
mat_data_MR = [matlab_data(:, 1:2), matlab_data(:, 99:122)];
mat_data_RR = [matlab_data(:, 1:2), matlab_data(:, 123:146)];

rec_data(1,:,:) = rec_data_FL;
rec_data(2,:,:) = rec_data_ML;
rec_data(3,:,:) = rec_data_RL;
rec_data(4,:,:) = rec_data_FR;
rec_data(5,:,:) = rec_data_MR;
rec_data(6,:,:) = rec_data_RR;

mat_data(1,:,:) = mat_data_FL;
mat_data(2,:,:) = mat_data_ML;
mat_data(3,:,:) = mat_data_RL;
mat_data(4,:,:) = mat_data_FR;
mat_data(5,:,:) = mat_data_MR;
mat_data(6,:,:) = mat_data_RR;

% base body
% figure
% set(gcf, 'Color', [1,1,1])
% for i = 1 : 6
%     subplot(2,3,i)
%     plot(recurdyn_data(:,2), recurdyn_data(:,i + 146), 'LineWidth', 2)
%     hold on
%     plot(matlab_data(:,2), matlab_data(:,i + 146), '--', 'LineWidth', 2)
%     grid on
%     xlabel('Time [sec]')
%     ylabel('Position [mm]')
% end
% 
% figure
% set(gcf, 'Color', [1,1,1])
% for i = 1 : 6
%     subplot(2,3,i)
%     plot(recurdyn_data(:,2), recurdyn_data(:,i + 146 + 6), 'LineWidth', 2)
%     hold on
%     plot(matlab_data(:,2), matlab_data(:,i + 146 + 6), '--', 'LineWidth', 2)
%     grid on
%     grid on
%     xlabel('Time [sec]')
%     ylabel('Velocity [mm/s]')
% end
% 
% figure
% set(gcf, 'Color', [1,1,1])
% for i = 1 : 6
%     subplot(2,3,i)
%     plot(recurdyn_data(:,2), recurdyn_data(:,i + 146 + 12), 'LineWidth', 2)
%     hold on
%     plot(matlab_data(:,2), matlab_data(:,i + 146 + 12), '--', 'LineWidth', 2)
%     grid on
%     grid on
%     xlabel('Time [sec]')
%     ylabel('Acceleration [mm/s^2]')
% end

for sindx = 1 : 1
    % q
    figure
    set(gcf, 'Color', [1.0 1.0 1.0])      % Figure 배경
    for i = 1 : 4
        subplot(3,4,i)
        plot(rec_data(sindx,:,2), rec_data(sindx,:,i+2), 'LineWidth', 2)
        hold on
        plot(mat_data(sindx,:,2), mat_data(sindx,:,i+2), '--', 'LineWidth', 2)
        grid on
        xlabel('Time [s]')
        ylabel('Displacement [rad]')
        t_txt = title(sprintf('subsystem %d, q%d', sindx, i));

        if i == 4
            lgd = legend('Ref', 'Analysis');
        end

        set(gca, 'FontSize', 13)
    end

    % dq
    % figure
    % set(gcf, 'Color', [1.0 1.0 1.0])      % Figure 배경
    for i = 1 : 4
        subplot(3,4,i+4)
        plot(rec_data(sindx,:,2), rec_data(sindx,:,i+8), 'LineWidth', 2)
        hold on
        plot(mat_data(sindx,:,2), mat_data(sindx,:,i+8), '--', 'LineWidth', 2)
        grid on
        xlabel('Time [s]')
        ylabel('Velocity [rad/s]')
        t_txt = title(sprintf('subsystem %d, dq%d', sindx, i));

        if i == 4
            lgd = legend('Ref', 'Analysis');
        end

        set(gca, 'FontSize', 13)
    end

    % ddq
    % figure
    % set(gcf, 'Color', [1.0 1.0 1.0])      % Figure 배경
    for i = 1 : 4
        subplot(3,4,i+8)
        plot(rec_data(sindx,:,2), rec_data(sindx,:,i+14), 'LineWidth', 2)
        hold on
        plot(mat_data(sindx,:,2), mat_data(sindx,:,i+14), '--', 'LineWidth', 2)
        grid on
        xlabel('Time [s]')
        ylabel('Acceleration [rad/s^2]')
        t_txt = title(sprintf('subsystem %d, ddq%d ', sindx, i));

        if i == 4
            lgd = legend('Ref', 'Analysis');
        end

        set(gca, 'FontSize', 13)
    end

    % EE pose
    figure
    set(gcf, 'Color', [1.0 1.0 1.0])      % Figure 배경
    for i = 1 : 6
        subplot(3,2,i)
        plot(rec_data(sindx,:,2), rec_data(sindx,:,i+20), 'LineWidth', 2)
        hold on
        plot(mat_data(sindx,:,2), mat_data(sindx,:,i+20), '--', 'LineWidth', 2)
        grid on
        xlabel('Time [s]')
        if i <= 3
            ylabel('Position [mm]')
        else
            ylabel('Angle [rad]')
        end
        t_txt = title(sprintf('subsystem %d, %s', sindx, ee_title_txt{i}));

        if i == 3
            lgd = legend('Ref', 'Analysis');
        end

        set(gca, 'FontSize', 13)
    end

end

% RSDA
for sindx = 1 : 6
    figure
    set(gcf, 'Color', [1,1,1])
    for i = 1 : 4
        subplot(2,2,i)
        plot(recurdyn_data(:,2), recurdyn_data(:,i+164+(sindx-1)*6), 'LineWidth', 2)
        hold on
        plot(matlab_data(:,2), matlab_data(:,i+164+(sindx-1)*6), 'LineWidth', 2)
        grid on
    end
end